"""Factorial free combinatorial counting helpers.

Computing binomial coefficients by cancelling factors avoids the overflow and
precision loss of building large factorials before dividing them.
"""
import logging

LOG = logging.getLogger(__name__)


def choose(n, k):
    """Return the binomial coefficient n choose k without factorials."""
    total = int(n)
    picks = int(k)
    if picks < 0 or picks > total:
        return 0
    picks = min(picks, total - picks)
    result = 1
    for step in range(1, picks + 1):
        result = result * (total - picks + step) // step
    return result


def permutations(n, k):
    """Return the number of ordered k-permutations of n items."""
    total = int(n)
    picks = int(k)
    if picks < 0 or picks > total:
        return 0
    result = 1
    for step in range(picks):
        result *= total - step
    return result


def pascal_row(n):
    """Return the nth row of Pascal's triangle."""
    size = int(n)
    row = [1]
    for index in range(1, size + 1):
        row.append(row[-1] * (size - index + 1) // index)
    return row


__all__ = ['choose', 'permutations', 'pascal_row']
