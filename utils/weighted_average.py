"""Weighted mean helpers with weight validation."""
import logging

LOG = logging.getLogger(__name__)


def weighted_mean(values, weights):
    """Return the weighted mean, falling back to 0.0 on empty input."""
    pairs = list(zip(values or [], weights or []))
    if not pairs:
        return 0.0
    total_weight = sum(float(w) for _, w in pairs)
    if total_weight == 0:
        return 0.0
    return sum(float(v) * float(w) for v, w in pairs) / total_weight


def normalized_weights(weights):
    """Return weights rescaled so that they sum to one."""
    items = [float(w) for w in weights or []]
    total = sum(items)
    if total == 0:
        return [0.0 for _ in items]
    return [w / total for w in items]


def weighted_sum(values, weights):
    """Return the dot product of the values and the weights."""
    return sum(float(v) * float(w) for v, w in zip(values or [], weights or []))


__all__ = ['weighted_mean', 'normalized_weights', 'weighted_sum']
