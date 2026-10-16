"""Exponentially weighted moving average smoothing.

Raw metric samples are noisy, so an EWMA provides a trend line that reacts
quickly to genuine level changes while suppressing single sample spikes.
"""
import logging

LOG = logging.getLogger(__name__)


def ewma(values, alpha=0.3):
    """Return the exponentially weighted moving average series."""
    if not 0.0 < alpha <= 1.0:
        raise ValueError('alpha must be in (0, 1]')
    smoothed = []
    current = None
    for value in values or []:
        if current is None:
            current = float(value)
        else:
            current = alpha * float(value) + (1.0 - alpha) * current
        smoothed.append(round(current, 4))
    LOG.debug('smoothed %d samples with alpha=%.2f', len(smoothed), alpha)
    return smoothed


def last_ewma(values, alpha=0.3):
    """Return only the final smoothed value, or None for an empty series."""
    series = ewma(values, alpha)
    return series[-1] if series else None


def half_life_alpha(half_life, interval=1.0):
    """Derive the smoothing factor that matches a desired half life."""
    if half_life <= 0 or interval <= 0:
        raise ValueError('half_life and interval must be positive')
    return round(1.0 - (0.5 ** (interval / float(half_life))), 4)


__all__ = ['ewma', 'last_ewma', 'half_life_alpha']
