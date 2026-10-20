"""Soundex code length audit.

Soundex keeps the first letter plus three digits; codes shorter than four
characters get right-padded with zeros.
"""
import logging

LOG = logging.getLogger(__name__)


def pad(code):
    """Return the Soundex code padded to four characters."""
    c = str(code or '')[:4]
    return c + '0' * max(0, 4 - len(c))


def collision_group(codes):
    """Return Soundex codes shared by more than one word."""
    from collections import Counter
    c = Counter(pad(x) for x in codes or [])
    shared = sorted(k for k, v in c.items() if v > 1)
    LOG.debug('soundex collision groups %d', len(shared))
    return shared


__all__ = ['pad', 'collision_group']
