"""Leaky bucket conformance check.

Bursts drain at the leak rate; a request conforms when the bucket holds fewer
than its capacity in drops.
"""
import logging

LOG = logging.getLogger(__name__)


def conform(level, capacity):
    """Report whether one more unit fits the bucket."""
    return float(level or 0) < float(capacity or 0)


def drain_wait_sec(level, capacity, leak_rate):
    """Return seconds until the bucket accepts one more unit."""
    if conform(level, capacity):
        return 0.0
    if not leak_rate or leak_rate <= 0:
        return float('inf')
    wait = (float(level) - float(capacity) + 1.0) / float(leak_rate)
    LOG.debug('leaky bucket wait %.3fs', wait)
    return round(wait, 3)


__all__ = ['conform', 'drain_wait_sec']
