"""Radian and degree conversion helpers."""
import logging
import math

LOG = logging.getLogger(__name__)

DEGREES_PER_RADIAN = 180.0 / math.pi


def to_degrees(radians):
    """Return the degree measure of an angle given in radians."""
    return radians * DEGREES_PER_RADIAN


def to_radians(degrees):
    """Return the radian measure of an angle given in degrees."""
    return degrees / DEGREES_PER_RADIAN


def degrees_series(radians):
    """Return every value converted from radians to degrees."""
    return [to_degrees(float(v)) for v in radians or []]


def radians_series(degrees):
    """Return every value converted from degrees to radians."""
    return [to_radians(float(v)) for v in degrees or []]


__all__ = ['to_degrees', 'to_radians', 'degrees_series', 'radians_series']
