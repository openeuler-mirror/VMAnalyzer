"""Interquartile range based outlier fencing.

The IQR fence marks points far from the bulk of the distribution without
assuming normality, which suits skewed metric data.
"""
import statistics
import logging

LOG = logging.getLogger(__name__)


def quartiles(values):
    """Return the first and third quartile of a series."""
    clean = sorted(float(v) for v in values or [] if v is not None)
    if not clean:
        LOG.debug('empty series, quartiles undefined')
        return None, None
    midpoint = len(clean) // 2
    lower = statistics.median(clean[:midpoint]) if midpoint else clean[0]
    upper_half = clean[midpoint + 1:] if len(clean) % 2 else clean[midpoint:]
    upper = statistics.median(upper_half) if upper_half else clean[-1]
    return round(lower, 5), round(upper, 5)


def fences(values, multiplier=1.5):
    """Return the lower and upper fence position for a series."""
    first, third = quartiles(values)
    if first is None:
        return None, None
    span = third - first
    return round(first - multiplier * span, 5), round(third + multiplier * span, 5)


def outside_fence(values, multiplier=1.5):
    """Return the samples falling outside the IQR fence."""
    low, high = fences(values, multiplier)
    if low is None:
        return []
    clean = [float(v) for v in values or [] if v is not None]
    return [value for value in clean if value < low or value > high]


__all__ = ['quartiles', 'fences', 'outside_fence']
