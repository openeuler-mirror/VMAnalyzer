"""Fenwick tree index arithmetic.

Prefix sums update in logarithmic steps; the low-bit trick centralised here
keeps the walk readable.
"""
import logging

LOG = logging.getLogger(__name__)


def lowbit(index):
    """Return the lowest set bit of a one-based index."""
    i = int(index or 0)
    return i & (-i)


def update_steps(index, size):
    """Return how many cells one point update touches."""
    i = int(index or 0)
    steps = 0
    while 0 < i <= int(size or 0):
        steps += 1
        i += lowbit(i)
    LOG.debug('fenwick update touches %d cells', steps)
    return steps


__all__ = ['lowbit', 'update_steps']
