"""Suggest hyphenation break points for English words."""
import re

__all__ = ["hyphenation_points", "hyphenate_word"]

_VOWELS = frozenset("aeiouy")


def hyphenation_points(word, min_len=5):
    """Return candidate syllable break positions within *word*."""
    text = re.sub(r"[^A-Za-z]", "", str(word)).lower()
    if len(text) < min_len:
        return []
    points = []
    for i in range(1, len(text)):
        if text[i] in _VOWELS and text[i - 1] not in _VOWELS:
            points.append(i)
    return [p for p in points if 1 < p < len(text) - 1]


def hyphenate_word(word, min_len=5, marker="\u00ad"):
    """Insert soft-hyphen markers at the suggested break points."""
    points = hyphenation_points(word, min_len)
    out, last = [], 0
    for point in points:
        out.append(str(word)[last:point])
        out.append(marker)
        last = point
    out.append(str(word)[last:])
    return "".join(out)
