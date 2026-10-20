"""Hilbert curve indexing.

Hilbert ordering keeps spatial neighbors adjacent on disk; xy2d maps a
grid cell to its curve position.
"""
import logging

LOG = logging.getLogger(__name__)


def _rot(n, x, y, rx, ry):
    if ry == 0:
        if rx == 1:
            x, y = n - 1 - x, n - 1 - y
        x, y = y, x
    return x, y


def xy2d(order, x, y):
    """Return the Hilbert distance of cell (x, y) on a 2^order grid."""
    n = 2 ** int(order)
    d, s = 0, n // 2
    while s > 0:
        rx = 1 if x & s else 0
        ry = 1 if y & s else 0
        d += s * s * ((3 * rx) ^ ry)
        x, y = _rot(s, x, y, rx, ry)
        s //= 2
    LOG.debug('hilbert d=%d for (%d,%d)', d, x, y)
    return d


__all__ = ['xy2d']
