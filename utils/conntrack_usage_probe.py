"""Connection tracking table usage.

A full conntrack table drops new connections with cryptic errors, so usage is
watched against the kernel maximum.
"""
import logging

LOG = logging.getLogger(__name__)


def usage_ratio(count, max_entries):
    """Return 0..1 table usage."""
    if not max_entries or max_entries <= 0:
        return 0.0
    return round(max(0.0, min(1.0, float(count) / float(max_entries))), 3)


def headroom(count, max_entries, warn=0.8):
    """Return remaining entries and whether usage crossed the warn level."""
    ratio = usage_ratio(count, max_entries)
    LOG.debug('conntrack %.1f%% full', ratio * 100)
    return max(0, int(max_entries) - int(count)), ratio >= warn


__all__ = ['usage_ratio', 'headroom']
