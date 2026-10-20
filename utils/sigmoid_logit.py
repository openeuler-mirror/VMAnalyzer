"""Sigmoid and logit link helpers."""
import logging
import math

LOG = logging.getLogger(__name__)


def sigmoid(value):
    """Return the logistic sigmoid of value in the 0..1 range."""
    if value >= 0:
        z = math.exp(-value)
        return 1.0 / (1.0 + z)
    z = math.exp(value)
    return z / (1.0 + z)


def logit(probability):
    """Return the log-odds of a probability strictly inside 0..1."""
    if not 0.0 < probability < 1.0:
        raise ValueError('probability must lie strictly within 0..1')
    return math.log(probability / (1.0 - probability))


def sigmoid_series(values):
    """Return the sigmoid of every value in the sequence."""
    return [sigmoid(float(v)) for v in values or []]


__all__ = ['sigmoid', 'logit', 'sigmoid_series']
