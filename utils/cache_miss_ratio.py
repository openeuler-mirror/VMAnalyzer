"""CPU cache miss ratio interpretation.

A rising last level cache miss ratio explains throughput loss that is invisible
in CPU utilisation, because stalled cycles still count as busy time.
"""
import logging

LOG = logging.getLogger(__name__)


def miss_ratio(misses, accesses):
    """Return the cache miss ratio for a counter pair."""
    total = int(accesses)
    if total <= 0:
        LOG.debug('no cache accesses recorded')
        return 0.0
    return round(min(1.0, int(misses) / float(total)), 4)


def ratio_delta(previous_ratio, current_ratio):
    """Return the change in miss ratio between two observations."""
    return round(float(current_ratio) - float(previous_ratio), 4)


def miss_verdict(ratio, warn=0.1, crit=0.3):
    """Classify cache behaviour as efficient, degraded or thrashing."""
    if ratio >= crit:
        return 'thrashing'
    if ratio >= warn:
        return 'degraded'
    return 'efficient'


__all__ = ['miss_ratio', 'ratio_delta', 'miss_verdict']
