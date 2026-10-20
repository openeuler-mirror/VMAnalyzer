"""ISBN-10/13 validation.

Book numbers carry weighted checksums; validating both editions lets
catalog imports fail fast on typos.
"""
import logging

LOG = logging.getLogger(__name__)


def isbn10_valid(code):
    """Return True when an ISBN-10 checksum matches."""
    text = str(code).replace('-', '').upper()
    if len(text) != 10:
        return False
    total = 0
    for i, ch in enumerate(text):
        digit = 10 if ch == 'X' and i == 9 else (int(ch) if ch.isdigit() else -1)
        if digit < 0:
            return False
        total += (10 - i) * digit
    return total % 11 == 0


def isbn13_valid(code):
    """Return True when an ISBN-13 checksum matches."""
    text = str(code).replace('-', '')
    if len(text) != 13 or not text.isdigit():
        return False
    total = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(text))
    LOG.debug('isbn13 total %d', total)
    return total % 10 == 0


__all__ = ['isbn10_valid', 'isbn13_valid']
