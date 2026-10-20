"""Normalise typographic quotes and dashes to ASCII equivalents."""
__all__ = ["normalize_quotes", "normalize_dashes", "normalize_typography", "has_typography"]

_QUOTES = {
    "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
    "\u00ab": '"', "\u00bb": '"', "\u2039": "'", "\u203a": "'",
}
_DASHES = {
    "\u2010": "-", "\u2011": "-", "\u2012": "-", "\u2013": "-",
    "\u2014": "--", "\u2212": "-",
}


def normalize_quotes(text):
    """Replace curly single/double quotes with straight ASCII quotes."""
    return "".join(_QUOTES.get(ch, ch) for ch in str(text))


def normalize_dashes(text):
    """Replace Unicode dash variants with ASCII hyphen equivalents."""
    return "".join(_DASHES.get(ch, ch) for ch in str(text))


def normalize_typography(text):
    """Apply both quote and dash normalisation to *text*."""
    return normalize_dashes(normalize_quotes(text))


def has_typography(text):
    """Return True when *text* contains curly quotes or Unicode dashes."""
    return any(ch in _QUOTES or ch in _DASHES for ch in str(text))
