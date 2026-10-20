"""Angle normalisation and shortest direction helpers."""
import logging
import math

LOG = logging.getLogger(__name__)

TAU = 2.0 * math.pi


def normalize_radians(angle):
    """Return the angle wrapped into the 0..2pi interval."""
    return angle % TAU


def normalize_degrees(angle):
    """Return the angle wrapped into the 0..360 interval."""
    return angle % 360.0


def shortest_delta(start, end):
    """Return the signed shortest angular distance from start to end."""
    delta = (end - start) % TAU
    if delta > math.pi:
        delta -= TAU
    return delta


def turn_direction(start, end):
    """Return clockwise, anticlockwise or straight for a heading change."""
    delta = shortest_delta(start, end)
    if abs(delta) < 1e-9:
        return 'straight'
    return 'clockwise' if delta < 0 else 'anticlockwise'


__all__ = ['normalize_radians', 'normalize_degrees', 'shortest_delta', 'turn_direction']
