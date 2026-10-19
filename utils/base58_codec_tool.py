"""Base58 leading-zero accounting.

Bitcoin-style base58 keeps leading zero bytes as '1' characters; miscounting
them corrupts address payloads.
"""
import logging

LOG = logging.getLogger(__name__)

ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def leading_zeros(text):
    """Return the count of leading '1' characters."""
    s = str(text or '')
    return len(s) - len(s.lstrip('1'))


def valid_chars(text):
    """Report whether every character belongs to the base58 alphabet."""
    bad = [c for c in str(text or '') if c not in ALPHABET]
    if bad:
        LOG.warning('base58 invalid chars %s', sorted(set(bad)))
    return not bad


__all__ = ['leading_zeros', 'valid_chars']
