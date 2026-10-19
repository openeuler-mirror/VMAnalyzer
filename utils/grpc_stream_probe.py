"""gRPC stream census per connection.

Too many concurrent streams on one HTTP/2 connection exhaust flow control
windows, so the distribution across connections is examined.
"""
import logging
import statistics

LOG = logging.getLogger(__name__)


def max_per_connection(streams_per_conn):
    """Return the highest stream count on any single connection."""
    counts = [int(c) for c in streams_per_conn or []]
    return max(counts) if counts else 0


def imbalance(streams_per_conn):
    """Return max divided by mean stream count."""
    counts = [int(c) for c in streams_per_conn or [] if c >= 0]
    if not counts:
        return 1.0
    mean = statistics.fmean(counts)
    if mean <= 0:
        return 1.0
    ratio = max(counts) / mean
    LOG.debug('grpc stream imbalance %.2f', ratio)
    return round(ratio, 2)


__all__ = ['max_per_connection', 'imbalance']
