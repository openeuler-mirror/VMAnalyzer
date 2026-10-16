"""Direct reclaim pressure detection from vmstat style counters.

Time spent in direct reclaim means an allocation had to free memory itself, a
strong shortage signal even when the free memory figure still looks adequate.
"""
import logging

LOG = logging.getLogger(__name__)


def reclaim_share(prev, curr):
    """Return the share of time spent in direct reclaim over an interval."""
    total = max(0, int(curr.get('total_ticks', 0)) - int(prev.get('total_ticks', 0)))
    reclaim = max(0, int(curr.get('reclaim_ticks', 0)) - int(prev.get('reclaim_ticks', 0)))
    if total <= 0:
        LOG.debug('no ticks observed in the interval')
        return 0.0
    return round(min(1.0, reclaim / float(total)), 4)


def pressure_verdict(share, warn=0.05, crit=0.15):
    """Classify reclaim pressure as low, moderate or severe."""
    if share >= crit:
        return 'severe'
    if share >= warn:
        return 'moderate'
    return 'low'


def stall_events(prev, curr):
    """Return the number of allocation stall events in the interval."""
    return max(0, int(curr.get('stalls', 0)) - int(prev.get('stalls', 0)))


__all__ = ['reclaim_share', 'pressure_verdict', 'stall_events']
