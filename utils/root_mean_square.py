"""Root mean square and peak to average ratio helpers."""
import logging
import math

LOG = logging.getLogger(__name__)


def root_mean_square(values):
    """Return the quadratic mean of a numeric sequence."""
    items = [float(v) for v in values or []]
    if not items:
        return 0.0
    return math.sqrt(sum(v * v for v in items) / len(items))


def mean_absolute_value(values):
    """Return the mean of the absolute sample magnitudes."""
    items = [abs(float(v)) for v in values or []]
    return sum(items) / len(items) if items else 0.0


def crest_factor(values):
    """Return the peak to RMS ratio of the samples."""
    items = [abs(float(v)) for v in values or []]
    if not items:
        return 0.0
    rms = root_mean_square(items)
    if rms == 0:
        return 0.0
    return max(items) / rms


__all__ = ['root_mean_square', 'mean_absolute_value', 'crest_factor']
