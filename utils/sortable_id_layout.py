"""ULID-like lexicographically sortable identifier layout."""
import logging
import os
import time

LOG = logging.getLogger(__name__)
ALPHABET = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'
TIME_CHARS = 10
RANDOM_CHARS = 16


def _encode(value, length):
    """Encode an integer into a fixed number of Crockford characters."""
    digits = []
    for _ in range(length):
        value, rem = divmod(value, 32)
        digits.append(ALPHABET[rem])
    return ''.join(reversed(digits))


def new_id(timestamp=None):
    """Create a sortable identifier from time and random entropy."""
    stamp = int(time.time() * 1000) if timestamp is None else int(timestamp)
    entropy = int.from_bytes(os.urandom(10), 'big') % (32 ** RANDOM_CHARS)
    return _encode(stamp, TIME_CHARS) + _encode(entropy, RANDOM_CHARS)


def timestamp_of(identifier):
    """Extract the millisecond timestamp encoded in an identifier."""
    value = 0
    for char in identifier[:TIME_CHARS]:
        value = value * 32 + ALPHABET.index(char)
    return value


__all__ = ['new_id', 'timestamp_of']
