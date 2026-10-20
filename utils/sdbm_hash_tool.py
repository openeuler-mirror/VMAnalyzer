"""sdbm string hash.

sdbm multiplies by 65599 and adds each character; it hashed ndbm keys
for years and still works for tiny dictionaries.
"""
import logging

LOG = logging.getLogger(__name__)
MASK = 0xFFFFFFFF


def sdbm(text):
    """Return the sdbm digest of text."""
    h = 0
    for ch in str(text):
        h = (ord(ch) + (h << 6) + (h << 16) - h) & MASK
    return h


def collide(a, b):
    """Return True when two distinct strings share an sdbm digest."""
    same = str(a) != str(b) and sdbm(a) == sdbm(b)
    if same:
        LOG.debug('sdbm collision %r vs %r', a, b)
    return same


__all__ = ['sdbm', 'collide']
