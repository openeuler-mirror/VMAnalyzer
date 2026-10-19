"""Virtqueue occupancy sampling.

A virtqueue that never drains means the backend cannot keep up, so occupancy
is sampled and averaged per queue.
"""
import logging

LOG = logging.getLogger(__name__)


def occupancy(used, size):
    """Return the 0..1 occupancy of one queue."""
    if not size or size <= 0:
        return 0.0
    return round(max(0.0, min(1.0, float(used) / float(size))), 3)


def mean_occupancy(samples):
    """Return the average occupancy across (used, size) sample pairs."""
    ratios = [occupancy(u, s) for u, s in samples or [] if s]
    if not ratios:
        return 0.0
    return round(sum(ratios) / float(len(ratios)), 3)


def backpressured(samples, watermark=0.9):
    """Report whether any sampled queue sat above the watermark."""
    hit = any(occupancy(u, s) >= watermark for u, s in samples or [] if s)
    if hit:
        LOG.debug('virtqueue backpressure detected')
    return hit


__all__ = ['occupancy', 'mean_occupancy', 'backpressured']
