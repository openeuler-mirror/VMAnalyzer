"""Redis keyspace hit ratio probe.

keyspace_hits and misses from INFO reveal cache effectiveness; a falling
ratio usually means the working set outgrew maxmemory.
"""
import logging

LOG = logging.getLogger(__name__)


def hit_ratio(hits, misses):
    """Return hits / (hits + misses) as a percentage."""
    total = int(hits) + int(misses)
    ratio = 0.0 if total == 0 else int(hits) * 100.0 / total
    LOG.debug('redis hit ratio %.2f%% over %d lookups', ratio, total)
    return round(ratio, 2)


def ratio_trend(samples):
    """Return rising/falling/flat from successive ratio samples."""
    vals = list(samples or [])
    if len(vals) < 2:
        return 'flat'
    delta = vals[-1] - vals[0]
    if abs(delta) < 0.5:
        return 'flat'
    return 'rising' if delta > 0 else 'falling'


__all__ = ['hit_ratio', 'ratio_trend']
