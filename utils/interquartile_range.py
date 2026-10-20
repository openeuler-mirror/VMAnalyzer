"""Interquartile range and Tukey fence helpers."""
import logging

LOG = logging.getLogger(__name__)


def quantile(values, fraction):
    """Return a linearly interpolated quantile for fraction in 0..1."""
    items = sorted(float(v) for v in values or [])
    if not items:
        return 0.0
    if not 0.0 <= fraction <= 1.0:
        raise ValueError('fraction must be within 0..1')
    position = fraction * (len(items) - 1)
    lower = int(position)
    upper = min(lower + 1, len(items) - 1)
    weight = position - lower
    return items[lower] * (1 - weight) + items[upper] * weight


def interquartile_range(values):
    """Return the spread between the 75th and 25th percentiles."""
    return quantile(values, 0.75) - quantile(values, 0.25)


def tukey_fences(values, factor=1.5):
    """Return the (lower, upper) fences used to flag mild outliers."""
    q1 = quantile(values, 0.25)
    q3 = quantile(values, 0.75)
    spread = q3 - q1
    return q1 - factor * spread, q3 + factor * spread


__all__ = ['quantile', 'interquartile_range', 'tukey_fences']
