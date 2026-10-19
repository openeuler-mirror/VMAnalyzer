"""Zram compression efficiency.

Zram trades CPU for memory; the memory saved is original minus compressed
bytes and should beat a configurable factor to stay worthwhile.
"""
import logging

LOG = logging.getLogger(__name__)


def saved_bytes(original, compressed):
    """Return bytes saved by compression."""
    return max(0, int(original or 0) - int(compressed or 0))


def worthwhile(original, compressed, factor=2.0):
    """Report when compression beats the requested factor."""
    comp = float(compressed or 0)
    if comp <= 0:
        return False
    ok = float(original or 0) / comp >= factor
    LOG.debug('zram factor %.2f ok=%s', float(original or 0) / comp, ok)
    return ok


__all__ = ['saved_bytes', 'worthwhile']
