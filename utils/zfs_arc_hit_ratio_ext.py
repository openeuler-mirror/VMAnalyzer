"""ZFS ARC cache hit ratio.

A falling ARC hit ratio means the working set outgrew the cache and reads now
hit spindles, so hits and misses are turned into a single ratio.
"""
import logging

LOG = logging.getLogger(__name__)


def hit_ratio(hits, misses):
    """Return the ARC hit ratio in 0..1."""
    h = float(hits or 0)
    m = float(misses or 0)
    if h + m <= 0:
        return 0.0
    return round(h / (h + m), 4)


def cache_verdict(ratio, floor=0.8):
    """Classify the cache as warm or cold."""
    verdict = 'warm' if ratio >= floor else 'cold'
    LOG.debug('arc ratio %.3f -> %s', ratio, verdict)
    return verdict


__all__ = ['hit_ratio', 'cache_verdict']
