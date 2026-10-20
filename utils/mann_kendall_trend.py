"""Mann-Kendall trend test.

Counting concordant minus discordant pairs yields the S statistic; its
sign detects monotone trends without assuming a distribution.
"""
import logging

LOG = logging.getLogger(__name__)


def s_statistic(series):
    """Return the Mann-Kendall S statistic."""
    vals = [float(v) for v in series or []]
    s = 0
    for i in range(len(vals)):
        for j in range(i + 1, len(vals)):
            diff = vals[j] - vals[i]
            s += 1 if diff > 0 else (-1 if diff < 0 else 0)
    return s


def trend(series, min_abs_s=3):
    """Return increasing/decreasing/none from the S statistic."""
    s = s_statistic(series)
    LOG.debug('mann-kendall S=%d', s)
    if s >= min_abs_s:
        return 'increasing'
    if s <= -min_abs_s:
        return 'decreasing'
    return 'none'


__all__ = ['s_statistic', 'trend']
