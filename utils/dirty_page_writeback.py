"""Dirty page writeback pacing.

When dirty pages accumulate faster than writeback drains them the kernel will
throttle writers hard, so the net rate decides how close we are.
"""
import logging

LOG = logging.getLogger(__name__)


def net_rate(dirtied_per_sec, written_per_sec):
    """Return the net pages per second accumulating in the dirty cache."""
    return round(float(dirtied_per_sec) - float(written_per_sec), 2)


def time_to_limit(dirty_pages, limit_pages, net_per_sec):
    """Return seconds until the dirty limit is reached, or None."""
    if net_per_sec <= 0:
        return None
    gap = float(limit_pages) - float(dirty_pages)
    if gap <= 0:
        return 0.0
    eta = gap / net_per_sec
    LOG.debug('dirty limit in %.1fs', eta)
    return round(eta, 1)


__all__ = ['net_rate', 'time_to_limit']
