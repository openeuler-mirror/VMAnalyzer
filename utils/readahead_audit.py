"""Readahead window effectiveness.

Read-ahead that is never consumed wastes bandwidth, so consumed pages are
compared to pages the kernel read ahead.
"""
import logging

LOG = logging.getLogger(__name__)


def efficiency(consumed_pages, readahead_pages):
    """Return the consumed share of read-ahead pages in 0..1."""
    if not readahead_pages or readahead_pages <= 0:
        return 0.0
    return round(min(1.0, float(consumed_pages or 0) / float(readahead_pages)), 3)


def shrink_advised(eff, floor=0.3):
    """Report when the window should shrink because reads go unused."""
    bad = eff < floor
    LOG.debug('readahead eff %.3f shrink=%s', eff, bad)
    return bad


__all__ = ['efficiency', 'shrink_advised']
