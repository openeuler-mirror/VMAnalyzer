"""ULID timestamp extraction.

A ULID starts with a 48-bit millisecond timestamp in Crockford base32;
decoding it recovers creation time without a database lookup.
"""
import logging
import time

LOG = logging.getLogger(__name__)
ALPHABET = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'


def timestamp_ms(ulid):
    """Return the millisecond timestamp encoded in the ULID prefix."""
    value = 0
    for ch in str(ulid)[:10].upper():
        value = value * 32 + ALPHABET.index(ch)
    return value


def age_seconds(ulid, now=None):
    """Return how many seconds ago the ULID was minted."""
    now = time.time() if now is None else now
    age = max(0.0, now - timestamp_ms(ulid) / 1000.0)
    LOG.debug('ulid age %.1fs', age)
    return round(age, 3)


__all__ = ['timestamp_ms', 'age_seconds', 'ALPHABET']
