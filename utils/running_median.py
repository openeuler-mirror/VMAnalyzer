"""Incremental running median over a sliding window."""
import logging
import statistics

LOG = logging.getLogger(__name__)


def running_median(values, window):
    """Return the median of each trailing window of the given size."""
    items = [float(v) for v in values or []]
    size = int(window)
    if size <= 0:
        raise ValueError('window must be positive')
    medians = []
    for index in range(len(items)):
        chunk = items[max(0, index - size + 1):index + 1]
        medians.append(statistics.median(chunk))
    return medians


def rolling_mad(values, window):
    """Return the rolling median absolute deviation over the window."""
    items = [float(v) for v in values or []]
    size = int(window)
    if size <= 0:
        raise ValueError('window must be positive')
    spreads = []
    for index in range(len(items)):
        chunk = items[max(0, index - size + 1):index + 1]
        centre = statistics.median(chunk)
        spreads.append(statistics.median([abs(v - centre) for v in chunk]))
    return spreads


def latest_median(values, window):
    """Return the median of the most recent window samples."""
    medians = running_median(values, window)
    return medians[-1] if medians else 0.0


__all__ = ['running_median', 'rolling_mad', 'latest_median']
