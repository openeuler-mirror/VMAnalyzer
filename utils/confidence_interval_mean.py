"""Confidence intervals for a sample mean."""
import logging
import math

LOG = logging.getLogger(__name__)

Z_95 = 1.959963984540054
Z_99 = 2.5758293035489004


def standard_error(values):
    """Return the standard error of the mean for the samples."""
    items = [float(v) for v in values or []]
    if len(items) < 2:
        return 0.0
    mean = sum(items) / len(items)
    variance = sum((v - mean) ** 2 for v in items) / (len(items) - 1)
    return math.sqrt(variance / len(items))


def mean_ci(values, z=Z_95):
    """Return the (low, high) confidence interval around the sample mean."""
    items = [float(v) for v in values or []]
    if not items:
        return 0.0, 0.0
    mean = sum(items) / len(items)
    margin = z * standard_error(items)
    return mean - margin, mean + margin


def margin_of_error(sigma, count, z=Z_95):
    """Return the confidence margin given a known population sigma."""
    if count <= 0:
        raise ValueError('count must be positive')
    return z * sigma / math.sqrt(count)


__all__ = ['standard_error', 'mean_ci', 'margin_of_error']
