"""FNV-1a hash.

FNV-1a is one multiply-xor per byte; the 32 and 64 bit variants share
the same loop with different constants.
"""
import logging

LOG = logging.getLogger(__name__)


def fnv1a(data, bits=32):
    """Return the FNV-1a digest at 32 or 64 bits."""
    if bits == 64:
        h, prime, mask = 0xCBF29CE484222325, 0x100000001B3, (1 << 64) - 1
    else:
        h, prime, mask = 0x811C9DC5, 0x01000193, 0xFFFFFFFF
    for byte in bytes(data):
        h = ((h ^ byte) * prime) & mask
    LOG.debug('fnv1a-%d=%x', bits, h)
    return h


def bucket_of(key, bucket_count):
    """Return the bucket index for a key using 64-bit FNV-1a."""
    return fnv1a(str(key).encode(), bits=64) % max(1, int(bucket_count))


__all__ = ['fnv1a', 'bucket_of']
