"""Fold accented Latin letters down to their ASCII base characters."""
import unicodedata

__all__ = ["fold_diacritics", "fold_text", "fold_lines"]


def fold_diacritics(text):
    """Return *text* with combining marks stripped from every char."""
    decomposed = unicodedata.normalize("NFD", str(text))
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))


def fold_text(text, drop_other=False):
    """Fold diacritics; optionally drop remaining non-ASCII characters."""
    folded = fold_diacritics(text)
    if not drop_other:
        return folded
    return folded.encode("ascii", "ignore").decode("ascii")


def fold_lines(lines):
    """Fold diacritics across an iterable of text lines."""
    return [fold_diacritics(line) for line in lines]
