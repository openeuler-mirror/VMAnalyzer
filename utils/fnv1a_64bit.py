"""FNV-1a 64 bit hash for stable bucketing."""
import logging

LOG = logging.getLogger(__name__)
OFFSET = 0xCBF29CE484222325
PRIME = 0x100000001B3
MASK = (1 << 64) - 1


def fnv1a_64(data):
    """Hash a bytes-like object with FNV-1a 64 bit."""
    digest = OFFSET
    for byte in data:
        digest ^= byte
        digest = (digest * PRIME) & MASK
    return digest


def fnv1a_64_text(text):
    """Hash a string after UTF-8 encoding."""
    return fnv1a_64(text.encode('utf-8'))


def bucket(key, buckets):
    """Map a key deterministically into a fixed number of buckets."""
    if buckets <= 0:
        raise ValueError('buckets must be positive')
    return fnv1a_64_text(key) % buckets


__all__ = ['fnv1a_64', 'fnv1a_64_text', 'bucket']
