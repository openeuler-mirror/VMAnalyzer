"""Numerically stable softmax normalisation."""
import logging
import math

LOG = logging.getLogger(__name__)


def softmax(values, temperature=1.0):
    """Return the softmax probabilities of a score sequence."""
    items = [float(v) for v in values or []]
    if not items:
        return []
    if temperature <= 0:
        raise ValueError('temperature must be positive')
    scaled = [v / temperature for v in items]
    peak = max(scaled)
    exponentials = [math.exp(v - peak) for v in scaled]
    total = sum(exponentials)
    return [value / total for value in exponentials]


def argmax_probability(values):
    """Return the most probable index and its softmax probability."""
    probabilities = softmax(values)
    if not probabilities:
        return 0, 0.0
    index = max(range(len(probabilities)), key=probabilities.__getitem__)
    return index, probabilities[index]


def entropy_from_scores(values):
    """Return the Shannon entropy in nats of the softmax distribution."""
    probabilities = softmax(values)
    return -sum(p * math.log(p) for p in probabilities if p > 0)


__all__ = ['softmax', 'argmax_probability', 'entropy_from_scores']
