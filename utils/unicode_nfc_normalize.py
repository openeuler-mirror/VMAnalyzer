"""Normalise strings to Unicode NFC / NFKC canonical forms."""
import unicodedata

__all__ = ["to_nfc", "to_nfkc", "same_normal_form", "is_nfc", "canonical_key"]


def to_nfc(text):
    """Return the NFC (canonical composition) form of *text*."""
    return unicodedata.normalize("NFC", str(text))


def to_nfkc(text):
    """Return the NFKC (compatibility composition) form of *text*."""
    return unicodedata.normalize("NFKC", str(text))


def same_normal_form(left, right):
    """Return True when both strings share one canonical NFC form."""
    return to_nfc(left) == to_nfc(right)


def is_nfc(text):
    """Return True when *text* is already in NFC form."""
    return str(text) == to_nfc(text)


def canonical_key(text):
    """Return an NFKC, case-folded key for tolerant comparisons."""
    return to_nfkc(text).casefold()
