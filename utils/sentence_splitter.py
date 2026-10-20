"""Split prose into sentences using punctuation heuristics."""
import re

__all__ = ["split_sentences", "count_sentences", "split_paragraphs"]

_BOUNDARY = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])")
_ABBREV = re.compile(r"\b(?:Mr|Mrs|Ms|Dr|Prof|St|vs|etc|e\.g|i\.e)\.")


def split_sentences(text):
    """Return a list of sentence strings extracted from *text*."""
    guarded = _ABBREV.sub(lambda m: m.group(0).replace(".", "\u0000"), str(text))
    parts = _BOUNDARY.split(guarded)
    return [p.replace("\u0000", ".").strip() for p in parts if p.strip()]


def count_sentences(text):
    """Return the number of sentences detected in *text*."""
    return len(split_sentences(text))


def split_paragraphs(text):
    """Return paragraphs, each split into its constituent sentences."""
    return [split_sentences(p) for p in str(text).split("\n\n") if p.strip()]
