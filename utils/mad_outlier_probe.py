"""Median absolute deviation outlier detection.

The median absolute deviation is resistant to the very outliers being searched
for, unlike the standard deviation which they inflate.
"""
import statistics
import logging

LOG = logging.getLogger(__name__)

SCALE = 1.4826


def mad(values):
    """Return the scaled median absolute deviation of a series."""
    clean = [float(v) for v in values or [] if v is not None]
    if not clean:
        LOG.debug('empty series, MAD undefined')
        return 0.0
    centre = statistics.median(clean)
    return round(SCALE * statistics.median([abs(v - centre) for v in clean]), 5)


def robust_scores(values):
    """Return each sample's deviation from the median in MAD units."""
    clean = [float(v) for v in values or [] if v is not None]
    deviation = mad(clean)
    if not clean or deviation == 0:
        return [0.0] * len(clean)
    centre = statistics.median(clean)
    return [round((value - centre) / deviation, 3) for value in clean]


def outliers(values, threshold=3.5):
    """Return the indices whose robust score exceeds the threshold."""
    return [index for index, score in enumerate(robust_scores(values))
            if abs(score) >= threshold]


__all__ = ['mad', 'robust_scores', 'outliers']
