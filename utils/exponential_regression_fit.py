"""Exponential curve fitting via log-linear least squares."""
import logging
import math

LOG = logging.getLogger(__name__)


def fit_exponential(xs, ys):
    """Return (scale, rate) for y = scale * exp(-rate * x) fitted by least squares."""
    pairs = [(float(x), float(y)) for x, y in zip(xs or [], ys or [])
             if float(y) > 0]
    if len(pairs) < 2:
        return 0.0, 0.0
    count = len(pairs)
    mean_x = sum(x for x, _ in pairs) / count
    mean_log = sum(math.log(y) for _, y in pairs) / count
    var_x = sum((x - mean_x) ** 2 for x, _ in pairs)
    if var_x == 0:
        return 0.0, 0.0
    cov = sum((x - mean_x) * (math.log(y) - mean_log) for x, y in pairs)
    slope = cov / var_x
    intercept = mean_log - slope * mean_x
    return math.exp(intercept), -slope


def predict(scale, rate, x):
    """Return the exponential prediction scale * exp(-rate * x)."""
    return scale * math.exp(-rate * x)


def decay_half_life(rate):
    """Return the x distance over which the exponential decays by half."""
    if rate <= 0:
        raise ValueError('rate must be positive')
    return math.log(2.0) / rate


__all__ = ['fit_exponential', 'predict', 'decay_half_life']
