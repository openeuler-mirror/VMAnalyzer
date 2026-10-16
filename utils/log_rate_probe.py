"""Log volume rate tracking for noisy services.

A sudden jump in log lines per second usually precedes an incident, while a drop
to zero often means the collection agent itself died.  These helpers track the
rate and detect silence.
"""
import logging

LOG = logging.getLogger(__name__)


def rate_per_second(counts, window_seconds):
    """Return the average line rate observed across a window."""
    total = sum(int(c) for c in counts or [])
    if window_seconds <= 0:
        LOG.debug('window must be positive')
        return 0.0
    return round(total / float(window_seconds), 3)


def silence_detected(counts, min_lines=1):
    """Report whether the log stream went silent in the window."""
    return sum(int(c) for c in counts or []) < min_lines


def burst_ratio(counts, baseline):
    """Return the ratio of the newest bucket against a baseline rate."""
    values = [int(c) for c in counts or []]
    if not values or baseline <= 0:
        return 0.0
    return round(values[-1] / float(baseline), 3)


__all__ = ['rate_per_second', 'silence_detected', 'burst_ratio']
