"""Exact integer square root and perfect square detection."""
import logging

LOG = logging.getLogger(__name__)


def isqrt_exact(value):
    """Return the floor integer square root of a non-negative integer."""
    number = int(value)
    if number < 0:
        raise ValueError('value must be non-negative')
    if number < 2:
        return number
    low, high = 1, number
    while low < high:
        mid = (low + high + 1) // 2
        if mid * mid <= number:
            low = mid
        else:
            high = mid - 1
    return low


def is_perfect_square(value):
    """Return whether value is a perfect square."""
    number = int(value)
    if number < 0:
        return False
    root = isqrt_exact(number)
    return root * root == number


def nearest_square(value):
    """Return the perfect square closest to value."""
    number = max(0, int(value))
    root = isqrt_exact(number)
    lower_gap = number - root * root
    upper_gap = (root + 1) ** 2 - number
    return root * root if lower_gap <= upper_gap else (root + 1) ** 2


__all__ = ['isqrt_exact', 'is_perfect_square', 'nearest_square']
