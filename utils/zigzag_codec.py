"""Zigzag signed mapping.

Signed deltas map to unsigned varints by zigzag folding; the round trip is
kept in one place to avoid sign bugs.
"""
import logging

LOG = logging.getLogger(__name__)


def encode(signed):
    """Return the zigzag unsigned mapping of the signed value."""
    v = int(signed or 0)
    return (v << 1) ^ (v >> 63) if v < 0 else v << 1


def decode(zigzagged):
    """Return the signed value of the zigzag mapping."""
    z = int(zigzagged or 0)
    val = (z >> 1) ^ -(z & 1)
    LOG.debug('zigzag %d -> %d', zigzagged, val)
    return val


__all__ = ['encode', 'decode']
