"""Morton (Z-order) coding.

Interleaving coordinate bits gives a cheap space-filling index used by
quadtrees and GPU texture layouts.
"""
import logging

LOG = logging.getLogger(__name__)


def _spread(v):
    v &= 0xFFFF
    v = (v | (v << 8)) & 0x00FF00FF
    v = (v | (v << 4)) & 0x0F0F0F0F
    v = (v | (v << 2)) & 0x33333333
    v = (v | (v << 1)) & 0x55555555
    return v


def morton_encode(x, y):
    """Return the Morton code of two 16-bit coordinates."""
    code = _spread(int(x)) | (_spread(int(y)) << 1)
    LOG.debug('morton %d,%d -> %d', x, y, code)
    return code


def morton_decode(code):
    """Return (x, y) from a Morton code."""

    def compact(v):
        v &= 0x55555555
        v = (v | (v >> 1)) & 0x33333333
        v = (v | (v >> 2)) & 0x0F0F0F0F
        v = (v | (v >> 4)) & 0x00FF00FF
        v = (v | (v >> 8)) & 0xFFFF
        return v

    return compact(int(code)), compact(int(code) >> 1)


__all__ = ['morton_encode', 'morton_decode']
