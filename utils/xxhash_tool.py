"""xxHash32 implementation.

xxHash trades cryptographic strength for speed; the 32-bit variant is
handy for shard keys and bloom filters.
"""
import logging

LOG = logging.getLogger(__name__)
P1, P2, P3, P4, P5 = 2654435761, 2246822519, 3266489917, 668265263, 374761393
MASK = 0xFFFFFFFF


def _rotl(value, count):
    return ((value << count) | (value >> (32 - count))) & MASK


def xxh32(data, seed=0):
    """Return the xxHash32 digest of bytes-like data."""
    buf = bytes(data)
    n = len(buf)
    h = (seed + P5) & MASK
    for byte in buf:
        h = (h + byte * P5) & MASK
        h = (_rotl(h, 11) * P1) & MASK
    h ^= n
    h ^= h >> 15
    h = (h * P2) & MASK
    h ^= h >> 13
    h = (h * P3) & MASK
    h ^= h >> 16
    LOG.debug('xxh32=%08x over %d bytes', h, n)
    return h


def shard_of(key, shard_count):
    """Return the shard index for a key."""
    return xxh32(str(key).encode()) % max(1, int(shard_count))


__all__ = ['xxh32', 'shard_of']
