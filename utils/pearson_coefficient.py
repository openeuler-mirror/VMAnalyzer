"""Pearson correlation coefficient for paired measurements."""
import logging
import math

LOG = logging.getLogger(__name__)


def pearson(xs, ys):
    """Return the Pearson correlation coefficient in the -1..1 range."""
    pairs = [(float(x), float(y)) for x, y in zip(xs or [], ys or [])]
    count = len(pairs)
    if count < 2:
        return 0.0
    mean_x = sum(x for x, _ in pairs) / count
    mean_y = sum(y for _, y in pairs) / count
    cov = sum((x - mean_x) * (y - mean_y) for x, y in pairs)
    var_x = sum((x - mean_x) ** 2 for x, _ in pairs)
    var_y = sum((y - mean_y) ** 2 for _, y in pairs)
    denominator = math.sqrt(var_x * var_y)
    if denominator == 0:
        return 0.0
    return cov / denominator


def correlation_strength(coefficient):
    """Classify a correlation coefficient into a verbal strength band."""
    magnitude = abs(coefficient)
    if magnitude >= 0.8:
        return 'strong'
    if magnitude >= 0.5:
        return 'moderate'
    if magnitude >= 0.3:
        return 'weak'
    return 'negligible'


__all__ = ['pearson', 'correlation_strength']
