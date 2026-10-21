"""Weighted random selection helpers built on the random module."""
import bisect
import logging
import random

LOG = logging.getLogger(__name__)


def cumulative_weights(weights):
    """Return the running cumulative sums of the weights."""
    running = 0.0
    cumulative = []
    for weight in weights or []:
        running += float(weight)
        cumulative.append(running)
    return cumulative


def weighted_choice(items, weights, rng=None):
    """Return one item chosen with probability proportional to its weight."""
    if not items:
        raise ValueError('items must not be empty')
    cumulative = cumulative_weights(weights)
    if not cumulative or cumulative[-1] <= 0:
        raise ValueError('weights must sum to a positive value')
    generator = rng or random
    point = generator.random() * cumulative[-1]
    index = bisect.bisect_right(cumulative, point)
    return items[min(index, len(items) - 1)]


def weighted_sample(items, weights, count, rng=None):
    """Return count items drawn independently with replacement."""
    return [weighted_choice(items, weights, rng) for _ in range(int(count))]


__all__ = ['cumulative_weights', 'weighted_choice', 'weighted_sample']
