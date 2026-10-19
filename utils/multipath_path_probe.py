"""Multipath path redundancy check.

Losing a path should never halve throughput unnoticed, so ready paths per
device are compared to the configured path count.
"""
import logging

LOG = logging.getLogger(__name__)


def ready_ratio(ready, configured):
    """Return ready/configured paths in 0..1."""
    if not configured or configured <= 0:
        return 0.0
    return round(min(1.0, max(0.0, float(ready or 0) / float(configured))), 3)


def lost_redundancy(ready, configured):
    """Report when fewer than two paths remain ready."""
    lost = int(ready or 0) < min(2, int(configured or 0))
    if lost:
        LOG.warning('multipath redundancy lost ready=%s of %s', ready, configured)
    return lost


__all__ = ['ready_ratio', 'lost_redundancy']
