"""djb2 string hash.

djb2 starts at 5381 and shifts-adds per character; the xor variant
spreads keys that only differ in the last byte.
"""
import logging

LOG = logging.getLogger(__name__)
MASK = 0xFFFFFFFF


def djb2(text):
    """Return the classic djb2 digest of text."""
    h = 5381
    for ch in str(text):
        h = ((h << 5) + h + ord(ch)) & MASK
    return h


def djb2a(text):
    """Return the xor variant of djb2."""
    h = 5381
    for ch in str(text):
        h = (((h << 5) + h) ^ ord(ch)) & MASK
    LOG.debug('djb2a=%08x', h)
    return h


__all__ = ['djb2', 'djb2a']
