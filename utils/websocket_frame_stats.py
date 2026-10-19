"""WebSocket frame size statistics.

Oversized frames stall the event loop of single threaded servers, so frame
sizes are summarised with a tail focus.
"""
import logging
import statistics

LOG = logging.getLogger(__name__)


def summarize(sizes):
    """Return count, mean and max frame size."""
    clean = [int(s) for s in sizes or [] if s is not None]
    if not clean:
        return {'count': 0}
    return {'count': len(clean), 'mean': round(statistics.fmean(clean), 1),
            'max': max(clean)}


def oversized(sizes, limit_bytes=65536):
    """Return how many frames exceeded the limit."""
    count = sum(1 for s in sizes or [] if int(s) > limit_bytes)
    LOG.debug('%d oversized frames', count)
    return count


__all__ = ['summarize', 'oversized']
