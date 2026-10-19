"""Memcached eviction pressure probe.

Evictions before item expiry mean the slab allocator ran out of room;
comparing evictions to current items sizes the pressure.
"""
import logging

LOG = logging.getLogger(__name__)


def eviction_ratio(evictions, curr_items):
    """Return evictions per live item, clamped at zero."""
    items = max(1, int(curr_items))
    ratio = max(0.0, float(evictions)) / items
    LOG.debug('memcached eviction ratio %.4f', ratio)
    return round(ratio, 4)


def pressure_level(evictions_per_min, warn=10, crit=100):
    """Return ok/warn/crit from evictions per minute."""
    rate = float(evictions_per_min)
    if rate >= crit:
        return 'crit'
    if rate >= warn:
        return 'warn'
    return 'ok'


__all__ = ['eviction_ratio', 'pressure_level']
