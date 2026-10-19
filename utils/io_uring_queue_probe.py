"""io_uring submission queue depth.

Submission queues that stay full mean the application outpaces the device, so
queue depth samples are summarised as occupancy.
"""
import logging

LOG = logging.getLogger(__name__)


def occupancy(depths, entries):
    """Return the mean queue occupancy in 0..1."""
    vals = [float(d) for d in depths or [] if d is not None]
    if not vals or not entries or entries <= 0:
        return 0.0
    mean = sum(vals) / len(vals)
    return round(min(1.0, mean / float(entries)), 3)


def full_windows(depths, entries):
    """Count samples where the queue was completely full."""
    full = sum(1 for d in depths or [] if d is not None and d >= entries)
    LOG.debug('io_uring full windows %d', full)
    return full


__all__ = ['occupancy', 'full_windows']
