"""Rounding numbers to a fixed number of significant figures."""
import logging
import math

LOG = logging.getLogger(__name__)


def order_of_magnitude(value):
    """Return the power of ten of the most significant digit of value."""
    if value == 0:
        return 0
    return int(math.floor(math.log10(abs(value))))


def round_sig(value, digits):
    """Return value rounded to the requested number of significant figures."""
    if digits <= 0:
        raise ValueError('digits must be positive')
    if value == 0:
        return 0.0
    magnitude = order_of_magnitude(value)
    factor = math.pow(10, digits - 1 - magnitude)
    return round(value * factor) / factor


def round_sig_all(values, digits):
    """Return every sample rounded to the given significant figures."""
    return [round_sig(float(v), digits) for v in values or []]


__all__ = ['order_of_magnitude', 'round_sig', 'round_sig_all']
