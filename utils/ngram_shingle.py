"""Produce character and word n-grams (shingles) from text."""
import re
from collections import Counter

__all__ = ["char_ngrams", "word_ngrams", "shingle_counts"]


def char_ngrams(text, n=3):
    """Return character n-grams from a whitespace-normalised string."""
    cleaned = re.sub(r"\s+", " ", str(text)).strip()
    return [cleaned[i:i + n] for i in range(max(0, len(cleaned) - n + 1))]


def word_ngrams(text, n=2):
    """Return tuples of consecutive words from *text*."""
    words = str(text).lower().split()
    return [tuple(words[i:i + n]) for i in range(max(0, len(words) - n + 1))]


def shingle_counts(text, n=3):
    """Return a Counter of character shingles within *text*."""
    return Counter(char_ngrams(text, n))
