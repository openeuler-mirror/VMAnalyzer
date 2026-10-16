"""Ordinary least squares slope fitting for capacity trends.

Fitting a straight line to a metric shows the long term direction independent of
short term noise, which is exactly what a capacity forecast needs.
"""
import statistics
import logging

LOG = logging.getLogger(__name__)


def fit_slope(values, interval=1.0):
    """Return the least squares slope for evenly spaced values."""
    clean = [float(v) for v in values or [] if v is not None]
    if len(clean) < 2 or interval <= 0:
        LOG.debug('insufficient points to fit a slope')
        return 0.0
    xs = [index * interval for index in range(len(clean))]
    mean_x = statistics.fmean(xs)
    mean_y = statistics.fmean(clean)
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, clean))
    denominator = sum((x - mean_x) ** 2 for x in xs)
    if denominator == 0:
        return 0.0
    return round(numerator / denominator, 5)


def fit_intercept(values, interval=1.0):
    """Return the intercept of the fitted line, or None when undefined."""
    clean = [float(v) for v in values or [] if v is not None]
    if len(clean) < 2 or interval <= 0:
        return None
    xs = [index * interval for index in range(len(clean))]
    return round(statistics.fmean(clean) - fit_slope(clean, interval) * statistics.fmean(xs), 5)


def trend_verdict(slope, flat_band=0.001):
    """Classify a fitted slope as flat, increasing or decreasing."""
    if abs(slope) <= flat_band:
        return 'flat'
    return 'increasing' if slope > 0 else 'decreasing'


__all__ = ['fit_slope', 'fit_intercept', 'trend_verdict']
