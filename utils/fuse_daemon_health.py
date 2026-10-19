"""FUSE daemon request latency.

A wedged FUSE daemon shows rising pending request counts; the pending queue is
compared to a small multiple of the worker count.
"""
import logging

LOG = logging.getLogger(__name__)


def pending_ratio(pending, workers):
    """Return pending requests per worker."""
    if not workers or workers <= 0:
        return float('inf') if pending else 0.0
    return round(float(pending or 0) / float(workers), 3)


def wedged(pending, workers, factor=4.0):
    """Report when the pending queue exceeds factor requests per worker."""
    bad = pending_ratio(pending, workers) > factor
    if bad:
        LOG.warning('fuse daemon wedged pending=%s workers=%s', pending, workers)
    return bad


__all__ = ['pending_ratio', 'wedged']
