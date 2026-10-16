"""Pearson correlation between two metric series.

Correlation helps narrow down which resource moves together with an observed
degradation before any causal claim is made.
"""
import math
import statistics
import logging

LOG = logging.getLogger(__name__)


def pearson(first, second):
    """Return the Pearson coefficient of two equal length series."""
    left = [float(v) for v in first or [] if v is not None]
    right = [float(v) for v in second or [] if v is not None]
    if len(left) != len(right) or len(left) < 2:
        LOG.debug('series differ in length or are too short to correlate')
        return 0.0
    mean_l = statistics.fmean(left)
    mean_r = statistics.fmean(right)
    cov = sum((a - mean_l) * (b - mean_r) for a, b in zip(left, right))
    spread_l = math.sqrt(sum((a - mean_l) ** 2 for a in left))
    spread_r = math.sqrt(sum((b - mean_r) ** 2 for b in right))
    if spread_l == 0 or spread_r == 0:
        return 0.0
    return round(cov / (spread_l * spread_r), 4)


def strength(value):
    """Classify the absolute correlation as none, weak, moderate or strong."""
    magnitude = abs(value)
    if magnitude >= 0.8:
        return 'strong'
    if magnitude >= 0.5:
        return 'moderate'
    if magnitude >= 0.2:
        return 'weak'
    return 'none'


def leading_pairs(pairs):
    """Return metric pairs ordered by descending correlation strength."""
    scored = [(name, pearson(a, b)) for name, a, b in pairs or []]
    return sorted(scored, key=lambda item: abs(item[1]), reverse=True)


__all__ = ['pearson', 'strength', 'leading_pairs']
