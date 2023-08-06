"""Module to tokenize email messages for spam filtering."""

from collections import deque
from itertools import chain
from itertools import islice
from urllib.parse import urlparse
import re
import unicodedata


skip_max_word_size = 12


##############################################################################
# To fold case or not to fold case?  I didn't want to fold case, because
# it hides information in English, and I have no idea what .lower() does
# to other languages; and, indeed, 'FREE' (all caps) turned out to be one
# of the strongest spam indicators in my content-only tests (== one with
# prob 0.99 *and* made it into spamprob's nbest list very often).
#
# Against preservering case, it makes the database size larger, and requires
# more training data to get enough "representative" mixed-case examples.
#
# Running my c.l.py tests didn't support my intuition that case was
# valuable, so it's getting folded away now.  Folding or not made no
# significant difference to the false positive rate, and folding made a
# small (but statistically significant all the same) reduction in the
# false negative rate.  There is one obvious difference:  after folding
# case, conference announcements no longer got high spam scores.  Their
# content was usually fine, but they were highly penalized for VISIT OUR
# WEBSITE FOR MORE INFORMATION! kinds of repeated SCREAMING.  That is
# indeed the language of advertising, and I halfway regret that folding
# away case no longer picks on them.
#
# Since the f-p rate didn't change, but conference announcements escaped
# that category, something else took their place.  It seems to be highly
# off-topic messages, like debates about Microsoft's place in the world.
# Talk about "money" and "lucrative" is indistinguishable now from talk
# about "MONEY" and "LUCRATIVE", and spam mentions MONEY a lot.


##############################################################################
# Character n-grams or words?
#
# With careful multiple-corpora c.l.py tests sticking to case-folded decoded
# text-only portions, and ignoring headers, and with identical special
# parsing & tagging of embedded URLs:
#
# Character 3-grams gave 5x as many false positives as split-on-whitespace
# (s-o-w).  The f-n rate was also significantly worse, but within a factor
# of 2.  So character 3-grams lost across the board.
#
# Character 5-grams gave 32% more f-ps than split-on-whitespace, but the
# s-o-w fp rate across 20,000 presumed-hams was 0.1%, and this is the
# difference between 23 and 34 f-ps.  There aren't enough there to say that's
# significnatly more with killer-high confidence.  There were plenty of f-ns,
# though, and the f-n rate with character 5-grams was substantially *worse*
# than with character 3-grams (which in turn was substantially worse than
# with s-o-w).
#
# Training on character 5-grams creates many more unique tokens than s-o-w:
# a typical run bloated to 150MB process size.  It also ran a lot slower than
# s-o-w, partly related to heavy indexing of a huge out-of-cache wordinfo
# dict.  I rarely noticed disk activity when running s-o-w, so rarely bothered
# to look at process size; it was under 30MB last time I looked.
#
# Figuring out *why* a msg scored as it did proved much more mysterious when
# working with character n-grams:  they often had no obvious "meaning".  In
# contrast, it was always easy to figure out what s-o-w was picking up on.
# 5-grams flagged a msg from Christian Tismer as spam, where he was discussing
# the speed of tasklets under his new implementation of stackless:
#
#     prob = 0.99999998959
#     prob('ed sw') = 0.01
#     prob('http0:pgp') = 0.01
#     prob('http0:python') = 0.01
#     prob('hlon ') = 0.99
#     prob('http0:wwwkeys') = 0.01
#     prob('http0:starship') = 0.01
#     prob('http0:stackless') = 0.01
#     prob('n xp ') = 0.99
#     prob('on xp') = 0.99
#     prob('p 150') = 0.99
#     prob('lon x') = 0.99
#     prob(' amd ') = 0.99
#     prob(' xp 1') = 0.99
#     prob(' athl') = 0.99
#     prob('1500+') = 0.99
#     prob('xp 15') = 0.99
#
# The spam decision was baffling until I realized that *all* the high-
# probablity spam 5-grams there came out of a single phrase:
#
#     AMD Athlon XP 1500+
#
# So Christian was punished for using a machine lots of spam tries to sell
# <wink>.  In a classic Bayesian classifier, this probably wouldn't have
# mattered, but Graham's throws away almost all the 5-grams from a msg,
# saving only the about-a-dozen farthest from a neutral 0.5.  So one bad
# phrase can kill you!  This appears to happen very rarely, but happened
# more than once.
#
# The conclusion is that character n-grams have almost nothing to recommend
# them under Graham's scheme:  harder to work with, slower, much larger
# database, worse results, and prone to rare mysterious disasters.
#
# There's one area they won hands-down:  detecting spam in what I assume are
# Asian languages.  The s-o-w scheme sometimes finds only line-ends to split
# on then, and then a "hey, this 'word' is way too big!  let's ignore it"
# gimmick kicks in, and produces no tokens at all.
#
# [Later:  we produce character 5-grams then under the s-o-w scheme, instead
# ignoring the blob, but only if there are high-bit characters in the blob;
# e.g., there's no point 5-gramming uuencoded lines, and doing so would
# bloat the database size.]
#
# Interesting:  despite that odd example above, the *kinds* of f-p mistakes
# 5-grams made were very much like s-o-w made -- I recognized almost all of
# the 5-gram f-p messages from previous s-o-w runs.  For example, both
# schemes have a particular hatred for conference announcements, although
# s-o-w stopped hating them after folding case.  But 5-grams still hate them.
# Both schemes also hate msgs discussing HTML with examples, with about equal
# passion.   Both schemes hate brief "please subscribe [unsubscribe] me"
# msgs, although 5-grams seems to hate them more.


##############################################################################
# How to tokenize?
#
# I started with string.split() merely for speed.  Over time I realized it
# was making interesting context distinctions qualitatively akin to n-gram
# schemes; e.g., "free!!" is a much stronger spam indicator than "free".  But
# unlike n-grams (whether word- or character- based) under Graham's scoring
# scheme, this mild context dependence never seems to go over the edge in
# giving "too much" credence to an unlucky phrase.
#
# OTOH, compared to "searching for words", it increases the size of the
# database substantially, less than but close to a factor of 2.  This is very
# much less than a word bigram scheme bloats it, but as always an increase
# isn't justified unless the results are better.
#
# Following are stats comparing
#
#    for token in text.split():  # left column
#
# to
#
#    for token in re.findall(r"[\w$\-\x80-\xff]+", text):  # right column
#
# text is case-normalized (text.lower()) in both cases, and the runs were
# identical in all other respects.  The results clearly favor the split()
# gimmick, although they vaguely suggest that some sort of compromise
# may do as well with less database burden; e.g., *perhaps* folding runs of
# "punctuation" characters into a canonical representative could do that.
# But the database size is reasonable without that, and plain split() avoids
# having to worry about how to "fold punctuation" in languages other than
# English.
#
#    false positive percentages
#        0.000  0.000  tied
#        0.000  0.050  lost
#        0.050  0.150  lost
#        0.000  0.025  lost
#        0.025  0.050  lost
#        0.025  0.075  lost
#        0.050  0.150  lost
#        0.025  0.000  won
#        0.025  0.075  lost
#        0.000  0.025  lost
#        0.075  0.150  lost
#        0.050  0.050  tied
#        0.025  0.050  lost
#        0.000  0.025  lost
#        0.050  0.025  won
#        0.025  0.000  won
#        0.025  0.025  tied
#        0.000  0.025  lost
#        0.025  0.075  lost
#        0.050  0.175  lost
#
#    won   3 times
#    tied  3 times
#    lost 14 times
#
#    total unique fp went from 8 to 20
#
#    false negative percentages
#        0.945  1.200  lost
#        0.836  1.018  lost
#        1.200  1.200  tied
#        1.418  1.636  lost
#        1.455  1.418  won
#        1.091  1.309  lost
#        1.091  1.272  lost
#        1.236  1.563  lost
#        1.564  1.855  lost
#        1.236  1.491  lost
#        1.563  1.599  lost
#        1.563  1.781  lost
#        1.236  1.709  lost
#        0.836  0.982  lost
#        0.873  1.382  lost
#        1.236  1.527  lost
#        1.273  1.418  lost
#        1.018  1.273  lost
#        1.091  1.091  tied
#        1.490  1.454  won
#
#    won   2 times
#    tied  2 times
#    lost 16 times
#
#    total unique fn went from 292 to 302
#
# Later:  Here's another tokenization scheme with more promise.
#
#     fold case, ignore punctuation, strip a trailing 's' from words (to
#     stop Guido griping about "hotel" and "hotels" getting scored as
#     distinct clues <wink>) and save both word bigrams and word unigrams
#
# This was the code:
#
#     # Tokenize everything in the body.
#     lastw = ''
#     for w in word_re.findall(text):
#         n = len(w)
#         # Make sure this range matches in tokenize_word().
#         if 3 <= n <= 12:
#             if w[-1] == 's':
#                 w = w[:-1]
#             yield w
#             if lastw:
#                 yield lastw + w
#             lastw = w + ' '
#
#         elif n >= 3:
#             lastw = ''
#             for t in tokenize_word(w):
#                 yield t
#
# where
#
#     word_re = re.compile(r"[\w$\-\x80-\xff]+")
#
# This at least doubled the process size.  It helped the f-n rate
# significantly, but probably hurt the f-p rate (the f-p rate is too low
# with only 4000 hams per run to be confident about changes of such small
# *absolute* magnitude -- 0.025% is a single message in the f-p table):
#
# false positive percentages
#     0.000  0.000  tied
#     0.000  0.075  lost  +(was 0)
#     0.050  0.125  lost  +150.00%
#     0.025  0.000  won   -100.00%
#     0.075  0.025  won    -66.67%
#     0.000  0.050  lost  +(was 0)
#     0.100  0.175  lost   +75.00%
#     0.050  0.050  tied
#     0.025  0.050  lost  +100.00%
#     0.025  0.000  won   -100.00%
#     0.050  0.125  lost  +150.00%
#     0.050  0.025  won    -50.00%
#     0.050  0.050  tied
#     0.000  0.025  lost  +(was 0)
#     0.000  0.025  lost  +(was 0)
#     0.075  0.050  won    -33.33%
#     0.025  0.050  lost  +100.00%
#     0.000  0.000  tied
#     0.025  0.100  lost  +300.00%
#     0.050  0.150  lost  +200.00%
#
# won   5 times
# tied  4 times
# lost 11 times
#
# total unique fp went from 13 to 21
#
# false negative percentages
#     0.327  0.218  won    -33.33%
#     0.400  0.218  won    -45.50%
#     0.327  0.218  won    -33.33%
#     0.691  0.691  tied
#     0.545  0.327  won    -40.00%
#     0.291  0.218  won    -25.09%
#     0.218  0.291  lost   +33.49%
#     0.654  0.473  won    -27.68%
#     0.364  0.327  won    -10.16%
#     0.291  0.182  won    -37.46%
#     0.327  0.254  won    -22.32%
#     0.691  0.509  won    -26.34%
#     0.582  0.473  won    -18.73%
#     0.291  0.255  won    -12.37%
#     0.364  0.218  won    -40.11%
#     0.436  0.327  won    -25.00%
#     0.436  0.473  lost    +8.49%
#     0.218  0.218  tied
#     0.291  0.255  won    -12.37%
#     0.254  0.364  lost   +43.31%
#
# won  15 times
# tied  2 times
# lost  3 times
#
# total unique fn went from 106 to 94

##############################################################################
# What about HTML?
#
# Computer geeks seem to view use of HTML in mailing lists and newsgroups as
# a mortal sin.  Normal people don't, but so it goes:  in a technical list/
# group, every HTML decoration has spamprob 0.99, there are lots of unique
# HTML decorations, and lots of them appear at the very start of the message
# so that Graham's scoring scheme latches on to them tight.  As a result,
# any plain text message just containing an HTML example is likely to be
# judged spam (every HTML decoration is an extreme).
#
# So if a message is multipart/alternative with both text/plain and text/html
# branches, we ignore the latter, else newbies would never get a message
# through.  If a message is just HTML, it has virtually no chance of getting
# through.
#
# In an effort to let normal people use mailing lists too <wink>, and to
# alleviate the woes of messages merely *discussing* HTML practice, I
# added a gimmick to strip HTML tags after case-normalization and after
# special tagging of embedded URLs.  This consisted of a regexp sub pattern,
# where instances got replaced by single blanks:
#
#    html_re = re.compile(r"""
#        <
#        [^\s<>]     # e.g., don't match 'a < b' or '<<<' or 'i << 5' or 'a<>b'
#        [^>]{0,128} # search for the end '>', but don't chew up the world
#        >
#    """, re.VERBOSE)
#
# and then
#
#    text = html_re.sub(' ', text)
#
# Alas, little good came of this:
#
#    false positive percentages
#        0.000  0.000  tied
#        0.000  0.000  tied
#        0.050  0.075  lost
#        0.000  0.000  tied
#        0.025  0.025  tied
#        0.025  0.025  tied
#        0.050  0.050  tied
#        0.025  0.025  tied
#        0.025  0.025  tied
#        0.000  0.050  lost
#        0.075  0.100  lost
#        0.050  0.050  tied
#        0.025  0.025  tied
#        0.000  0.025  lost
#        0.050  0.050  tied
#        0.025  0.025  tied
#        0.025  0.025  tied
#        0.000  0.000  tied
#        0.025  0.050  lost
#        0.050  0.050  tied
#
#    won   0 times
#    tied 15 times
#    lost  5 times
#
#    total unique fp went from 8 to 12
#
#    false negative percentages
#        0.945  1.164  lost
#        0.836  1.418  lost
#        1.200  1.272  lost
#        1.418  1.272  won
#        1.455  1.273  won
#        1.091  1.382  lost
#        1.091  1.309  lost
#        1.236  1.381  lost
#        1.564  1.745  lost
#        1.236  1.564  lost
#        1.563  1.781  lost
#        1.563  1.745  lost
#        1.236  1.455  lost
#        0.836  0.982  lost
#        0.873  1.309  lost
#        1.236  1.381  lost
#        1.273  1.273  tied
#        1.018  1.273  lost
#        1.091  1.200  lost
#        1.490  1.599  lost
#
#    won   2 times
#    tied  1 times
#    lost 17 times
#
#    total unique fn went from 292 to 327
#
# The messages merely discussing HTML were no longer fps, so it did what it
# intended there.  But the f-n rate nearly doubled on at least one run -- so
# strong a set of spam indicators is the mere presence of HTML.  The increase
# in the number of fps despite that the HTML-discussing msgs left that
# category remains mysterious to me, but it wasn't a significant increase
# so I let it drop.
#
# Later:  If I simply give up on making mailing lists friendly to my sisters
# (they're not nerds, and create wonderfully attractive HTML msgs), a
# compromise is to strip HTML tags from only text/plain msgs.  That's
# principled enough so far as it goes, and eliminates the HTML-discussing
# false positives.  It remains disturbing that the f-n rate on pure HTML
# msgs increases significantly when stripping tags, so the code here doesn't
# do that part.  However, even after stripping tags, the rates above show that
# at least 98% of spams are still correctly identified as spam.
#
# So, if another way is found to slash the f-n rate, the decision here not
# to strip HTML from HTML-only msgs should be revisited.
#
# Later, after the f-n rate got slashed via other means:
#
# false positive percentages
#     0.000  0.000  tied
#     0.000  0.000  tied
#     0.050  0.075  lost   +50.00%
#     0.025  0.025  tied
#     0.075  0.025  won    -66.67%
#     0.000  0.000  tied
#     0.100  0.100  tied
#     0.050  0.075  lost   +50.00%
#     0.025  0.025  tied
#     0.025  0.000  won   -100.00%
#     0.050  0.075  lost   +50.00%
#     0.050  0.050  tied
#     0.050  0.025  won    -50.00%
#     0.000  0.000  tied
#     0.000  0.000  tied
#     0.075  0.075  tied
#     0.025  0.025  tied
#     0.000  0.000  tied
#     0.025  0.025  tied
#     0.050  0.050  tied
#
# won   3 times
# tied 14 times
# lost  3 times
#
# total unique fp went from 13 to 11
#
# false negative percentages
#     0.327  0.400  lost   +22.32%
#     0.400  0.400  tied
#     0.327  0.473  lost   +44.65%
#     0.691  0.654  won     -5.35%
#     0.545  0.473  won    -13.21%
#     0.291  0.364  lost   +25.09%
#     0.218  0.291  lost   +33.49%
#     0.654  0.654  tied
#     0.364  0.473  lost   +29.95%
#     0.291  0.327  lost   +12.37%
#     0.327  0.291  won    -11.01%
#     0.691  0.654  won     -5.35%
#     0.582  0.655  lost   +12.54%
#     0.291  0.400  lost   +37.46%
#     0.364  0.436  lost   +19.78%
#     0.436  0.582  lost   +33.49%
#     0.436  0.364  won    -16.51%
#     0.218  0.291  lost   +33.49%
#     0.291  0.400  lost   +37.46%
#     0.254  0.327  lost   +28.74%
#
# won   5 times
# tied  2 times
# lost 13 times
#
# total unique fn went from 106 to 122
#
# So HTML decorations are still a significant clue when the ham is composed
# of c.l.py traffic.  Again, this should be revisited if the f-n rate is
# slashed again.
#
# Later:  As the amount of training data increased, the effect of retaining
# HTML tags decreased to insignificance.  options.retain_pure_html_tags
# was introduced to control this, and it defaulted to False.  Later, as the
# algorithm improved, retain_pure_html_tags was removed.
#
# Later:  The decision to ignore "redundant" HTML is also dubious, since
# the text/plain and text/html alternatives may have entirely different
# content.  options.ignore_redundant_html was introduced to control this,
# and it defaults to False.  Later:  ignore_redundant_html was also removed.

##############################################################################
# How big should "a word" be?
#
# As I write this, words less than 3 chars are ignored completely, and words
# with more than 12 are special-cased, replaced with a summary "I skipped
# about so-and-so many chars starting with such-and-such a letter" token.
# This makes sense for English if most of the info is in "regular size"
# words.
#
# A test run boosting to 13 had no effect on f-p rate, and did a little
# better or worse than 12 across runs -- overall, no significant difference.
# The database size is smaller at 12, so there's nothing in favor of 13.
# A test at 11 showed a slight but consistent bad effect on the f-n rate
# (lost 12 times, won once, tied 7 times).
#
# A test with no lower bound showed a significant increase in the f-n rate.
# Curious, but not worth digging into.  Boosting the lower bound to 4 is a
# worse idea:  f-p and f-n rates both suffered significantly then.  I didn't
# try testing with lower bound 2.
#
# Anthony Baxter found that boosting the option skip_max_word_size to 20
# from its default of 12 produced a quite dramatic decrease in the number
# of 'unsure' messages.  However, this was coupled with a large increase
# in the FN rate, and it remains unclear whether simply shifting cutoffs
# would have given the same tradeoff (not enough data was posted to tell).
#
# On Tim's c.l.py test, 10-fold CV, ham_cutoff=0.20 and spam_cutoff=0.80:
#
# -> <stat> tested 2000 hams & 1400 spams against 18000 hams & 12600 spams
# [ditto]
#
# filename:    max12   max20
# ham:spam:  20000:14000
#                    20000:14000
# fp total:        2       2       the same
# fp %:         0.01    0.01
# fn total:        0       0       the same
# fn %:         0.00    0.00
# unsure t:      103     100       slight decrease
# unsure %:     0.30    0.29
# real cost:  $40.60  $40.00       slight improvement with these cutoffs
# best cost:  $27.00  $27.40       best possible got slightly worse
# h mean:       0.28    0.27
# h sdev:       2.99    2.92
# s mean:      99.94   99.93
# s sdev:       1.41    1.47
# mean diff:   99.66   99.66
# k:           22.65   22.70
#
# "Best possible" in max20 would have been to boost ham_cutoff to 0.50(!),
# and drop spam_cutoff a little to 0.78.  This would have traded away most
# of the unsures in return for letting 3 spam through:
#
# -> smallest ham & spam cutoffs 0.5 & 0.78
# ->     fp 2; fn 3; unsure ham 11; unsure spam 11
# ->     fp rate 0.01%; fn rate 0.0214%; unsure rate 0.0647%
#
# Best possible in max12 was much the same:
#
# -> largest ham & spam cutoffs 0.5 & 0.78
# ->     fp 2; fn 3; unsure ham 12; unsure spam 8
# ->     fp rate 0.01%; fn rate 0.0214%; unsure rate 0.0588%
#
# The classifier pickle size increased by about 1.5 MB (~8.4% bigger).
#
# Rob Hooft's results were worse:
#
# -> <stat> tested 1600 hams & 580 spams against 14400 hams & 5220 spams
# [...]
# -> <stat> tested 1600 hams & 580 spams against 14400 hams & 5220 spams
# filename:   skip12  skip20
# ham:spam:  16000:5800
#                     16000:5800
# fp total:       12      13
# fp %:         0.07    0.08
# fn total:        7       7
# fn %:         0.12    0.12
# unsure t:      178     184
# unsure %:     0.82    0.84
# real cost: $162.60 $173.80
# best cost: $106.20 $109.60
# h mean:       0.51    0.52
# h sdev:       4.87    4.92
# s mean:      99.42   99.39
# s sdev:       5.22    5.34
# mean diff:   98.91   98.87
# k:            9.80    9.64

has_highbit_char = re.compile(r"[\x80-\xff]").search


def tokenize_text(
    text,
    maxword=skip_max_word_size,
    restrict_charset=None,
    replace_nonascii_chars=False,
):

    if replace_nonascii_chars:
        restrict_charset = "ascii"

    # Normalize case and unicode form
    text = unicodedata.normalize("NFKC", text.lower())

    if restrict_charset:
        # Replace high-bit chars and control chars with '?'.
        text = text.encode(restrict_charset, "replace").decode(restrict_charset)

    for w in text.split():
        n = len(w)
        if n >= 3:
            # Make sure this range matches in tokenize_word().
            if n <= maxword:
                yield w

            else:
                yield from tokenize_word(w, maxword=maxword)


def tokenize_word(word, _len=len, maxword=skip_max_word_size, generate_long_skips=True):
    n = _len(word)

    if n < 3:
        return

    # Make sure this range matches in tokenize().
    if n <= maxword:
        yield word

    else:
        # A long word.

        # Don't want to skip embedded email addresses.
        # An earlier scheme also split up the y in x@y on '.'.  Not splitting
        # improved the f-n rate; the f-p rate didn't care either way.
        if "://" in word:
            yield "url:1"
            yield from tokenize_url(word)
        if "." in word and word.count("@") == 1:
            yield "email:1"
            yield from tokenize_email(word)
        else:
            # There's value in generating a token indicating roughly how
            # many chars were skipped.  This has real benefit for the f-n
            # rate, but is neutral for the f-p rate.  I don't know why!
            # XXX Figure out why, and/or see if some other way of summarizing
            # XXX this info has greater benefit.
            if generate_long_skips:
                yield "skip:%c %d" % (word[0], n // 10 * 10)
            if has_highbit_char(word):
                hicount = 0
                for i in map(ord, word):
                    if i >= 128:
                        hicount += 1
                yield "8bit%%:%d" % round(hicount * 100.0 / len(word))


def tokenize_url(word):
    try:
        domain = ".".join(urlparse(word).netloc.split(".")[:-2])
    except ValueError:
        yield "url:invalid"
    else:
        yield f"url:{domain}"


def tokenize_email(word):
    try:
        p1, p2 = word.split("@")
        yield f"email name:{p1}"
        yield f"email addr:{p2}"
    except ValueError:
        yield f"email:{word}"


def add_sparse_bigrams(tokens, n=3):
    tokens = iter(tokens)
    window = deque(islice(tokens, n), maxlen=n)
    push = window.append
    windowsize = len(window)
    if windowsize == 0:
        return
    elif windowsize < n:
        window.extend([None] * (n - windowsize))
    for token in chain(tokens, [None] * (n - 1)):
        first = None
        for ix, tok in enumerate(window):
            if ix == 0:
                first = tok
                if tok:
                    yield tok
            elif tok:
                yield f"{first}{'_' * ix}{tok}"
        push(token)
