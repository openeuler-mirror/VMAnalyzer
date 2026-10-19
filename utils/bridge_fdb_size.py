"""Bridge forwarding table size tracking.

An FDB that keeps growing past expectations usually means a loop or a spoofed
source, so entry counts are compared with a capacity budget.
"""
import logging

LOG = logging.getLogger(__name__)


def usage_ratio(entries, capacity):
    """Return 0..1 usage of the forwarding table."""
    if not capacity or capacity <= 0:
        return 0.0
    return round(max(0.0, min(1.0, float(entries) / float(capacity))), 3)


def growth_per_min(samples, interval_sec=60.0):
    """Return the per minute entry growth from a sample series."""
    clean = [int(s) for s in samples or [] if s is not None]
    if len(clean) < 2 or interval_sec <= 0:
        return 0.0
    span = float(interval_sec) * (len(clean) - 1)
    rate = (clean[-1] - clean[0]) / span * 60.0
    LOG.debug('fdb growth %.2f/min', rate)
    return round(rate, 2)


__all__ = ['usage_ratio', 'growth_per_min']
