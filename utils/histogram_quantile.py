"""Quantile estimation from a bucketed histogram.

Cumulative buckets only bound a quantile, so linear interpolation inside the
containing bucket recovers an estimate good enough for latency reporting.
"""
import logging

LOG = logging.getLogger(__name__)


def quantile(bucket_bounds, cumulative_counts, target):
    """Estimate a quantile by interpolation inside the containing bucket."""
    if not bucket_bounds or not cumulative_counts:
        return None
    if not 0.0 <= target <= 1.0:
        raise ValueError('target must be within 0 and 1')
    total = cumulative_counts[-1]
    if total <= 0:
        return None
    goal = target * total
    lower_bound = 0.0
    lower_count = 0.0
    for bound, count in zip(bucket_bounds, cumulative_counts):
        if count >= goal:
            if count == lower_count:
                return float(bound)
            fraction = (goal - lower_count) / float(count - lower_count)
            LOG.debug('interpolated quantile inside bucket %s', bound)
            return round(lower_bound + fraction * (bound - lower_bound), 4)
        lower_bound = bound
        lower_count = count
    return float(bucket_bounds[-1])


def quantile_error(bucket_bounds, cumulative_counts, target, observed):
    """Return the absolute error of an estimate against a known value."""
    estimate = quantile(bucket_bounds, cumulative_counts, target)
    if estimate is None:
        return None
    return round(abs(estimate - observed), 4)


def bucket_widths(bucket_bounds):
    """Return the width of each histogram bucket."""
    widths = []
    previous = 0.0
    for bound in bucket_bounds:
        widths.append(round(bound - previous, 4))
        previous = bound
    return widths


__all__ = ['quantile', 'quantile_error', 'bucket_widths']
