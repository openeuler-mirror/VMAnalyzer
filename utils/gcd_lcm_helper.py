"""Greatest common divisor and least common multiple helpers."""
import logging
import math

LOG = logging.getLogger(__name__)


def gcd_pair(a, b):
    """Return the greatest common divisor of two integers."""
    return math.gcd(int(a), int(b))


def gcd_many(values):
    """Return the greatest common divisor across a sequence of integers."""
    result = 0
    for value in values or []:
        result = math.gcd(result, int(value))
    return result


def lcm_pair(a, b):
    """Return the least common multiple of two integers."""
    left, right = abs(int(a)), abs(int(b))
    if left == 0 or right == 0:
        return 0
    return left // math.gcd(left, right) * right


def lcm_many(values):
    """Return the least common multiple across a sequence of integers."""
    result = 1
    for value in values or []:
        result = lcm_pair(result, value)
    return result


__all__ = ['gcd_pair', 'gcd_many', 'lcm_pair', 'lcm_many']
