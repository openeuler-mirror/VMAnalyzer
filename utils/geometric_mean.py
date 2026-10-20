"""Geometric mean helpers for multiplicative quantities."""
import logging
import math

LOG = logging.getLogger(__name__)


def geometric_mean(values):
    """Return the geometric mean, or 0.0 when the input is empty."""
    items = [float(v) for v in values or []]
    if not items:
        return 0.0
    if any(v < 0 for v in items):
        raise ValueError('geometric mean requires non-negative values')
    if any(v == 0 for v in items):
        return 0.0
    return math.exp(sum(math.log(v) for v in items) / len(items))


def geometric_growth_rate(start, end, periods):
    """Return the per-period compound growth factor between two levels."""
    if start <= 0 or end <= 0 or periods <= 0:
        raise ValueError('start, end and periods must be positive')
    return (end / float(start)) ** (1.0 / periods)


def compound_growth(values):
    """Return the mean per-step growth factor over consecutive samples."""
    items = [float(v) for v in values or []]
    ratios = [items[i + 1] / items[i]
              for i in range(len(items) - 1) if items[i] > 0]
    return geometric_mean(ratios)


__all__ = ['geometric_mean', 'geometric_growth_rate', 'compound_growth']
