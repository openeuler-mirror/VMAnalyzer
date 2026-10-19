"""Orphan TCP socket tracking.

Orphaned sockets are not attached to any process yet still consume memory;
a rising count signals a leaking application.
"""
import logging

LOG = logging.getLogger(__name__)


def growth_rate(samples, interval_sec=60.0):
    """Return orphans per second from cumulative samples."""
    clean = [float(s) for s in samples or [] if s is not None]
    if len(clean) < 2 or interval_sec <= 0:
        return 0.0
    span = float(interval_sec) * (len(clean) - 1)
    return round((clean[-1] - clean[0]) / span, 2)


def over_limit(count, limit, watermark=0.8):
    """Report when the count crosses the watermark share of the limit."""
    if limit <= 0:
        return False
    hit = float(count) / float(limit) >= watermark
    LOG.debug('orphans %d/%d', count, limit)
    return hit


__all__ = ['growth_rate', 'over_limit']
