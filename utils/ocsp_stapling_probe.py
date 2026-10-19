"""OCSP staple freshness.

A stale stapled response breaks clients once it expires; freshness is the
share of validity already consumed.
"""
import logging

LOG = logging.getLogger(__name__)


def freshness(this_update_ts, next_update_ts, now_ts):
    """Return 0..1 remaining validity of the stapled response."""
    total = float(next_update_ts or 0) - float(this_update_ts or 0)
    if total <= 0:
        return 0.0
    left = float(next_update_ts or 0) - float(now_ts or 0)
    return round(max(0.0, min(1.0, left / total)), 3)


def renew_due(fresh, floor=0.25):
    """Report when the staple should be renewed."""
    due = float(fresh or 0) <= floor
    LOG.debug('ocsp freshness %.3f renew=%s', fresh, due)
    return due


__all__ = ['freshness', 'renew_due']
