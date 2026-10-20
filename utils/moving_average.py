"""Simple and cumulative moving averages over numeric streams."""
import logging

LOG = logging.getLogger(__name__)


def simple_moving_average(values, window):
    """Return the trailing simple moving average for every sample."""
    items = [float(v) for v in values or []]
    if window <= 0:
        raise ValueError('window must be positive')
    out = []
    for index in range(len(items)):
        chunk = items[max(0, index - window + 1):index + 1]
        out.append(sum(chunk) / len(chunk))
    return out


def cumulative_moving_average(values):
    """Return the running mean of all samples seen so far."""
    items = [float(v) for v in values or []]
    out = []
    total = 0.0
    for index, value in enumerate(items, start=1):
        total += value
        out.append(total / index)
    return out


def windowed_average(values, window):
    """Return the mean of the last window samples, or 0.0 when empty."""
    items = [float(v) for v in values or []]
    if not items:
        return 0.0
    chunk = items[-window:] if window > 0 else items
    return sum(chunk) / len(chunk)


__all__ = ['simple_moving_average', 'cumulative_moving_average', 'windowed_average']
