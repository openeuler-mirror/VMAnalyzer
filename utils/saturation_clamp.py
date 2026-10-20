"""Saturation and clamping helpers for bounded metrics."""
import logging

LOG = logging.getLogger(__name__)


def clamp(value, low, high):
    """Return value constrained to the inclusive low..high interval."""
    if low > high:
        raise ValueError('low must not exceed high')
    return max(low, min(high, value))


def saturate(value, high, low=0.0):
    """Return value clipped into the low..high saturation band."""
    return clamp(value, low, high)


def clamp_all(values, low, high):
    """Return every sample clamped into the low..high interval."""
    return [clamp(float(v), low, high) for v in values or []]


def soft_clamp(value, high):
    """Return value compressed smoothly as its magnitude grows past high."""
    if high <= 0:
        raise ValueError('high must be positive')
    ratio = abs(value) / (high + abs(value))
    return high * ratio if value >= 0 else -high * ratio


__all__ = ['clamp', 'saturate', 'clamp_all', 'soft_clamp']
