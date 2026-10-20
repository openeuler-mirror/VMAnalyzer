"""Robust outlier clipping based on the median absolute deviation."""
import logging
import statistics

LOG = logging.getLogger(__name__)

DEFAULT_THRESHOLD = 3.5


def mad_bounds(values, threshold=DEFAULT_THRESHOLD):
    """Return robust (lower, upper) bounds derived from median and MAD."""
    items = [float(v) for v in values or []]
    if not items:
        return 0.0, 0.0
    centre = statistics.median(items)
    deviation = statistics.median([abs(v - centre) for v in items])
    if deviation == 0:
        return centre, centre
    return centre - threshold * deviation, centre + threshold * deviation


def clip_outliers(values, threshold=DEFAULT_THRESHOLD):
    """Return values with entries beyond the MAD bounds pulled onto them."""
    lower, upper = mad_bounds(values, threshold)
    return [min(max(float(v), lower), upper) for v in values or []]


def outlier_indices(values, threshold=DEFAULT_THRESHOLD):
    """Return the indices of values lying outside the MAD bounds."""
    lower, upper = mad_bounds(values, threshold)
    return [index for index, v in enumerate(values or [])
            if not lower <= float(v) <= upper]


__all__ = ['mad_bounds', 'clip_outliers', 'outlier_indices']
