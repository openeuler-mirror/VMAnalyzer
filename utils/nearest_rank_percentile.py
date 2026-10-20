"""Nearest-rank percentile selection without any third party library.

The nearest-rank method picks the smallest sample whose rank covers the
requested percentile.  It never interpolates, so results are always real
observed values rather than synthetic estimates.
"""
import logging
import math

LOG = logging.getLogger(__name__)


def percentile_rank(values, percent):
    """Return the nearest-rank percentile of values for percent in 0..100."""
    items = sorted(float(v) for v in values or [])
    if not items:
        return 0.0
    if not 0 <= percent <= 100:
        raise ValueError('percent must be within 0..100')
    rank = max(1, math.ceil(percent / 100.0 * len(items)))
    return items[rank - 1]


def median(values):
    """Return the 50th nearest-rank percentile."""
    return percentile_rank(values, 50)


def quartiles(values):
    """Return the (q1, q2, q3) nearest-rank quartiles."""
    return (
        percentile_rank(values, 25),
        percentile_rank(values, 50),
        percentile_rank(values, 75),
    )


__all__ = ['percentile_rank', 'median', 'quartiles']
