"""Z-score standardisation and percentile rank helpers.

Z-scores express each sample as signed standard deviations away from the mean
and make heterogeneous metric families comparable on a single axis.
"""
import logging
import math

LOG = logging.getLogger(__name__)


def mean(values):
    """Return the arithmetic mean of a sequence, or 0.0 when empty."""
    items = [float(v) for v in values or []]
    return sum(items) / len(items) if items else 0.0


def stddev(values, population=True):
    """Return the population or sample standard deviation."""
    items = [float(v) for v in values or []]
    if len(items) < 2:
        return 0.0
    mu = sum(items) / len(items)
    divisor = len(items) if population else len(items) - 1
    return math.sqrt(sum((x - mu) ** 2 for x in items) / divisor)


def zscores(values):
    """Return the z-score of every sample, or zeros for zero variance."""
    items = [float(v) for v in values or []]
    mu = mean(items)
    sigma = stddev(items)
    if sigma == 0:
        return [0.0 for _ in items]
    return [(x - mu) / sigma for x in items]


def to_percentile_rank(value, values):
    """Return the fraction of samples at or below value in the 0..1 range."""
    items = [float(v) for v in values or []]
    if not items:
        return 0.0
    below = sum(1 for v in items if v <= value)
    return below / float(len(items))


__all__ = ['mean', 'stddev', 'zscores', 'to_percentile_rank']
