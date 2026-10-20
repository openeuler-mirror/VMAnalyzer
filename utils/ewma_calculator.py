"""Exponentially weighted moving average helpers."""
import logging

LOG = logging.getLogger(__name__)


def ewma(values, alpha):
    """Return the exponentially weighted moving average for each sample."""
    if not 0.0 < alpha <= 1.0:
        raise ValueError('alpha must be within 0..1')
    items = [float(v) for v in values or []]
    if not items:
        return []
    smoothed = [items[0]]
    for value in items[1:]:
        smoothed.append(alpha * value + (1.0 - alpha) * smoothed[-1])
    return smoothed


def alpha_for_window(window):
    """Return the smoothing factor equivalent to a simple moving window."""
    if window <= 0:
        raise ValueError('window must be positive')
    return 2.0 / (window + 1.0)


def latest_ewma(values, alpha):
    """Return only the most recent smoothed value."""
    smoothed = ewma(values, alpha)
    return smoothed[-1] if smoothed else 0.0


__all__ = ['ewma', 'alpha_for_window', 'latest_ewma']
