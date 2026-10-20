"""Population count and bit position helpers."""
import logging

LOG = logging.getLogger(__name__)


def popcount(value):
    """Return the number of set bits in a non-negative integer."""
    number = int(value)
    if number < 0:
        raise ValueError('value must be non-negative')
    return bin(number).count('1')


def popcount_many(values):
    """Return the population counts for every value in the sequence."""
    return [popcount(v) for v in values or []]


def lowest_set_bit(value):
    """Return the index of the least significant set bit, or -1 if none."""
    number = int(value)
    if number == 0:
        return -1
    return (number & -number).bit_length() - 1


def highest_set_bit(value):
    """Return the index of the most significant set bit, or -1 if none."""
    number = int(value)
    return number.bit_length() - 1 if number > 0 else -1


__all__ = ['popcount', 'popcount_many', 'lowest_set_bit', 'highest_set_bit']
