"""Count word frequencies, optionally after stopword removal."""
import re
from collections import Counter

__all__ = ["count_words", "top_words"]

STOPWORDS = frozenset({
    "the", "a", "an", "of", "and", "or", "to", "in", "is", "it", "for", "on", "with",
})
_TOKEN = re.compile(r"[a-z0-9']+")


def count_words(text, ignore_stopwords=True, stopwords=STOPWORDS):
    """Return a Counter of lower-cased word tokens found in *text*."""
    tokens = _TOKEN.findall(str(text).lower())
    if ignore_stopwords:
        tokens = [t for t in tokens if t not in stopwords]
    return Counter(tokens)


def top_words(text, limit=10, **kwargs):
    """Return the *limit* most frequent ``(word, count)`` pairs."""
    return count_words(text, **kwargs).most_common(limit)
