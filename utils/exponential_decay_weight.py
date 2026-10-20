"""Exponential decay weighting for recency biased aggregation."""
import logging
import math

LOG = logging.getLogger(__name__)


def decay_weights(count, half_life):
    """Return weights decaying by half every half_life steps, newest first."""
    if count <= 0:
        return []
    if half_life <= 0:
        raise ValueError('half_life must be positive')
    return [math.pow(0.5, index / float(half_life)) for index in range(count)]


def weighted_recent_mean(values, half_life):
    """Return the recency weighted mean, newest sample first."""
    items = [float(v) for v in values or []]
    if not items:
        return 0.0
    weights = decay_weights(len(items), half_life)
    total = sum(weights)
    return sum(w * v for w, v in zip(weights, items)) / total


def effective_window(half_life):
    """Return the number of samples that hold half of the total weight."""
    if half_life <= 0:
        raise ValueError('half_life must be positive')
    return 2.0 * half_life


__all__ = ['decay_weights', 'weighted_recent_mean', 'effective_window']
