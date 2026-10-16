"""Sanitizer for free text fields flowing into logs and reports.

Untrusted strings may carry control characters or unbounded length, both of
which corrupt downstream parsing, so they are normalised before use.
"""
import unicodedata
import logging

LOG = logging.getLogger(__name__)

PRINTABLE = set(range(32, 127))


def strip_control(text):
    """Return the text with control characters replaced by spaces."""
    cleaned = []
    for char in str(text):
        code = ord(char)
        if char in ('\n', '\t') or code in PRINTABLE or code >= 160:
            cleaned.append(char)
        else:
            cleaned.append(' ')
    return ''.join(cleaned)


def clamp(text, max_len=255, suffix='...'):
    """Truncate the text to max_len characters, appending a marker."""
    text = str(text)
    if len(text) <= max_len:
        return text
    keep = max(0, max_len - len(suffix))
    return text[:keep] + suffix


def sanitize(text, max_len=255):
    """Normalise unicode, strip control characters and clamp the length."""
    normalised = unicodedata.normalize('NFKC', str(text))
    return clamp(strip_control(normalised).strip(), max_len)


__all__ = ['strip_control', 'clamp', 'sanitize']
