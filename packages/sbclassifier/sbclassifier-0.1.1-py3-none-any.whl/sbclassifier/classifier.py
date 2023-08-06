# An implementation of a Bayes-like spam classifier.
#
# Paul Graham's original description:
#
#     http://www.paulgraham.com/spam.html
#
# A highly fiddled version of that can be retrieved from our CVS repository,
# via tag Last-Graham.  This made many demonstrated improvements in error
# rates over Paul's original description.
#
# This code implements Gary Robinson's suggestions, the core of which are
# well explained on his webpage:
#
#    http://radio.weblogs.com/0101454/stories/2002/09/16/spamDetection.html
#
# This is theoretically cleaner, and in testing has performed at least as
# well as our highly tuned Graham scheme did, often slightly better, and
# sometimes much better.  It also has "a middle ground", which people like:
# the scores under Paul's scheme were almost always very near 0 or very near
# 1, whether or not the classification was correct.  The false positives
# and false negatives under Gary's basic scheme (use_gary_combining) generally
# score in a narrow range around the corpus's best spam_cutoff value.
# However, it doesn't appear possible to guess the best spam_cutoff value in
# advance, and it's touchy.
#
# The last version of the Gary-combining scheme can be retrieved from our
# CVS repository via tag Last-Gary.
#
# The chi-combining scheme used by default here gets closer to the theoretical
# basis of Gary's combining scheme, and does give extreme scores, but also
# has a very useful middle ground (small # of msgs spread across a large range
# of scores, and good cutoff values aren't touchy).
#
# This implementation is due to Tim Peters et alia.

import math as _math

from sbclassifier.chi2 import chi2Q


class Classifier:

    use_bigrams = False
    unknown_word_prob = 0.5
    unknown_word_strength = 0.45
    minimum_prob_strength = 0.1
    ham_cutoff = 0.2
    spam_cutoff = 0.9
    max_discriminators = 150

    def __init__(self, classifier_db):
        self.db = classifier_db
        self.probcache = {}

    # spamprob using the chi-squared implementation
    # Across vectors of length n, containing random uniformly-distributed
    # probabilities, -2*sum(ln(p_i)) follows the chi-squared distribution
    # with 2*n degrees of freedom.  This has been proven (in some
    # appropriate sense) to be the most sensitive possible test for
    # rejecting the hypothesis that a vector of probabilities is uniformly
    # distributed.  Gary Robinson's original scheme was monotonic *with*
    # this test, but skipped the details.  Turns out that getting closer
    # to the theoretical roots gives a much sharper classification, with
    # a very small (in # of msgs), but also very broad (in range of scores),
    # "middle ground", where most of the mistakes live.  In particular,
    # this scheme seems immune to all forms of "cancellation disease":  if
    # there are many strong ham *and* spam clues, this reliably scores
    # close to 0.5.  Most other schemes are extremely certain then -- and
    # often wrong.
    def spamprob(
        self,
        wordstream,
        evidence=False,
        ln=_math.log,
        frexp=_math.frexp,
        LN2=_math.log(2),
    ):
        """
        Return best-guess probability that wordstream is spam.

        wordstream is an iterable object producing words.
        The return value is a float in [0.0, 1.0].

        If optional arg evidence is True, the return value is a pair
            probability, evidence
        where evidence is a list of (word, probability) pairs.
        """
        # We compute two chi-squared statistics, one for ham and one for
        # spam.  The sum-of-the-logs business is more sensitive to probs
        # near 0 than to probs near 1, so the spam measure uses 1-p (so
        # that high-spamprob words have greatest effect), and the ham
        # measure uses p directly (so that lo-spamprob words have greatest
        # effect).
        #
        # For optimization, sum-of-logs == log-of-product, and f.p.
        # multiplication is a lot cheaper than calling ln().  It's easy
        # to underflow to 0.0, though, so we simulate unbounded dynamic
        # range via frexp.  The real product H = this H * 2**Hexp, and
        # likewise the real product S = this S * 2**Sexp.
        H = S = 1.0
        Hexp = Sexp = 0

        clues = self._getclues(wordstream)
        for prob, word, record in clues:
            S *= 1.0 - prob
            H *= prob
            if S < 1e-200:  # prevent underflow
                S, e = frexp(S)
                Sexp += e
            if H < 1e-200:  # prevent underflow
                H, e = frexp(H)
                Hexp += e

        # Compute the natural log of the product = sum of the logs:
        # ln(x * 2**i) = ln(x) + i * ln(2).
        S = ln(S) + Sexp * LN2
        H = ln(H) + Hexp * LN2

        n = len(clues)
        if n:
            S = 1.0 - chi2Q(-2.0 * S, 2 * n)
            H = 1.0 - chi2Q(-2.0 * H, 2 * n)

            # How to combine these into a single spam score?  We originally
            # used (S-H)/(S+H) scaled into [0., 1.], which equals S/(S+H).  A
            # systematic problem is that we could end up being near-certain
            # a thing was (for example) spam, even if S was small, provided
            # that H was much smaller.
            # Rob Hooft stared at these problems and invented the measure
            # we use now, the simpler S-H, scaled into [0., 1.].
            prob = (S - H + 1.0) / 2.0
        else:
            prob = 0.5

        if evidence:
            clues = [(w, p) for p, w, _r in clues]
            clues.sort(key=lambda a: a[1])
            clues.insert(0, ("*S*", S))
            clues.insert(0, ("*H*", H))
            return prob, clues
        else:
            return prob

    def learn(self, wordstream, is_spam):
        """Teach the classifier by example.

        wordstream is a word stream representing a message.  If is_spam is
        True, you're telling the classifier this message is definitely spam,
        else that it's definitely not spam.
        """
        self._add_msg(wordstream, is_spam)

    def unlearn(self, wordstream, is_spam):
        """In case of pilot error, call unlearn ASAP after screwing up.

        Pass the same arguments you passed to learn().
        """
        self._remove_msg(wordstream, is_spam)

    def clear(self):
        """
        Reset the training database
        """
        self.db.clear()
        self.probcache.clear()

    def probability(self, record):
        """Compute, store, and return prob(msg is spam | msg contains word).

        This is the Graham calculation, but stripped of biases, and
        stripped of clamping into 0.01 thru 0.99.  The Bayesian
        adjustment following keeps them in a sane range, and one
        that naturally grows the more evidence there is to back up
        a probability.
        """

        spamcount = record.spamcount
        hamcount = record.hamcount

        # Try the cache first
        try:
            return self.probcache[spamcount][hamcount]
        except KeyError:
            pass

        nham = float(self.db.nham or 1)
        nspam = float(self.db.nspam or 1)

        assert hamcount <= nham, "Token seen in more ham than ham trained."
        hamratio = hamcount / nham

        assert spamcount <= nspam, "Token seen in more spam than spam trained."
        spamratio = spamcount / nspam

        prob = spamratio / (hamratio + spamratio)

        S = self.unknown_word_strength
        StimesX = S * self.unknown_word_prob

        # Now do Robinson's Bayesian adjustment.
        #
        #         s*x + n*p(w)
        # f(w) = --------------
        #           s + n
        #
        # I find this easier to reason about like so (equivalent when
        # s != 0):
        #
        #        x - p
        #  p +  -------
        #       1 + n/s
        #
        # IOW, it moves p a fraction of the distance from p to x, and
        # less so the larger n is, or the smaller s is.

        n = hamcount + spamcount
        prob = (StimesX + n * prob) / (S + n)

        # Update the cache
        try:
            self.probcache[spamcount][hamcount] = prob
        except KeyError:
            self.probcache[spamcount] = {hamcount: prob}

        return prob

    # NOTE:  Graham's scheme had a strange asymmetry:  when a word appeared
    # n>1 times in a single message, training added n to the word's hamcount
    # or spamcount, but predicting scored words only once.  Tests showed
    # that adding only 1 in training, or scoring more than once when
    # predicting, hurt under the Graham scheme.
    # This isn't so under Robinson's scheme, though:  results improve
    # if training also counts a word only once.  The mean ham score decreases
    # significantly and consistently, ham score variance decreases likewise,
    # mean spam score decreases (but less than mean ham score, so the spread
    # increases), and spam score variance increases.
    # I (Tim) speculate that adding n times under the Graham scheme helped
    # because it acted against the various ham biases, giving frequently
    # repeated spam words (like "Viagra") a quick ramp-up in spamprob; else,
    # adding only once in training, a word like that was simply ignored until
    # it appeared in 5 distinct training spams.  Without the ham-favoring
    # biases, though, and never ignoring words, counting n times introduces
    # a subtle and unhelpful bias.
    # There does appear to be some useful info in how many times a word
    # appears in a msg, but distorting spamprob doesn't appear a correct way
    # to exploit it.
    def _add_msg(self, wordstream, is_spam):
        self.probcache = {}  # nuke the prob cache
        if is_spam:
            self.db.nspam += 1
        else:
            self.db.nham += 1

        for word in set(wordstream):
            try:
                record = self.db[word]
            except KeyError:
                record = WordInfo()

            if is_spam:
                record.spamcount += 1
            else:
                record.hamcount += 1

            self.db[word] = record

        self._post_training()

    def _remove_msg(self, wordstream, is_spam):
        self.probcache = {}  # nuke the prob cache
        if is_spam:
            if self.db.nspam <= 0:
                raise ValueError("spam count would go negative!")
            self.db.nspam -= 1
        else:
            if self.db.nham <= 0:
                raise ValueError("non-spam count would go negative!")
            self.db.nham -= 1

        wordinfoget = self.db.get
        for word in set(wordstream):
            record = wordinfoget(word)
            if record is not None:
                if is_spam:
                    if record.spamcount > 0:
                        record.spamcount -= 1
                else:
                    if record.hamcount > 0:
                        record.hamcount -= 1
                if record.hamcount == 0 == record.spamcount:
                    del self.db[word]
                else:
                    self.db[word] = record

        self._post_training()

    def _post_training(self):
        """This is called after training on a wordstream.  Subclasses might
        want to ensure that their databases are in a consistent state at
        this point.  Introduced to fix bug #797890."""
        pass

    def _getclues(self, wordstream):
        """
        Return list of (prob, word, record) triples, sorted by increasing
        probability.

        "word" is a token from wordstream; "prob" is its spamprob (a
        float in 0.0 through 1.0); and "record" is word's associated
        WordInfo record if word is in the training database, or None if it's
        not.

        No more than max_discriminators items are returned, and have
        the strongest (farthest from 0.5) spamprobs of all tokens in wordstream.
        Tokens with spamprobs less than minimum_prob_strength away from 0.5
        aren't returned.
        """
        mindist = self.minimum_prob_strength

        clues = []
        push = clues.append
        for word in set(wordstream):
            tup = self._worddistanceget(word)
            if tup[0] >= mindist:
                push(tup)
        clues.sort()

        if len(clues) > self.max_discriminators:
            del clues[: -self.max_discriminators]
        # Return (prob, word, record).
        return [t[1:] for t in clues]

    def _worddistanceget(self, word):
        try:
            record = self.db[word]
        except KeyError:
            record = None
            prob = self.unknown_word_prob
        else:
            prob = self.probability(record)
        distance = abs(prob - 0.5)
        return distance, prob, word, record


class WordInfo(object):
    """
    A WordInfo is created for each distinct word.  spamcount is the
    number of trained spam msgs in which the word appears, and hamcount
    the number of trained ham msgs.

    Invariant:  For use in a classifier database, at least one of
    spamcount and hamcount must be non-zero.

    Important:  This is a tiny object.  Use of __slots__ is essential
    to conserve memory.
    """

    __slots__ = "spamcount", "hamcount"

    def __init__(self):
        self.__setstate__((0, 0))

    def __repr__(self):
        return "WordInfo" + repr((self.spamcount, self.hamcount))

    def __getstate__(self):
        return self.spamcount, self.hamcount

    def __setstate__(self, t):
        self.spamcount, self.hamcount = t


class ClassifierDb(dict):
    def __init__(self):
        super().__init__(self)
        self.nspam = 0
        self.nham = 0

    def clear(self):
        super().clear()
        self.nspam = 0
        self.nham = 0
