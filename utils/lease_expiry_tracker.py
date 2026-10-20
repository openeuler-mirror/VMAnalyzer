"""Lease expiry sweep.

DHCP and lock leases expire silently; the tracker ranks leases by seconds
remaining so the reaper runs in order.
"""
import logging

LOG = logging.getLogger(__name__)


def seconds_left(expires_ts, now_ts):
    """Return remaining lease seconds, floored at zero."""
    return max(0.0, float(expires_ts or 0) - float(now_ts or 0))


def reap_order(leases, now_ts):
    """Return lease names ordered by soonest expiry."""
    order = sorted((leases or {}).items(), key=lambda kv: seconds_left(kv[1], now_ts))
    names = [name for name, _ in order]
    LOG.debug('reap order %s', names[:5])
    return names


__all__ = ['seconds_left', 'reap_order']
