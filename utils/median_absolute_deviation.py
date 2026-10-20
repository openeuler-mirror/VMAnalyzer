"""Median absolute deviation and robust spread estimation.

MAD is the median of absolute deviations from the median.  Unlike the standard
deviation it is not inflated by a handful of extreme samples.
"""
import logging

LOG = logging.getLogger(__name__)

SCALE_CONSTANT = 1.4826


def median(values):
    """Return the median of a sequence, or 0.0 when empty."""
    items = sorted(float(v) for v in values or [])
    if not items:
        return 0.0
    mid = len(items) // 2
    if len(items) % 2:
        return items[mid]
    return (items[mid - 1] + items[mid]) / 2.0


def median_absolute_deviation(values):
    """Return the raw median absolute deviation of the samples."""
    items = [float(v) for v in values or []]
    if not items:
        return 0.0
    centre = median(items)
    return median([abs(x - centre) for x in items])


def robust_sigma(values):
    """Return the MAD scaled to be comparable with a standard deviation."""
    return median_absolute_deviation(values) * SCALE_CONSTANT


__all__ = ['median', 'median_absolute_deviation', 'robust_sigma']
