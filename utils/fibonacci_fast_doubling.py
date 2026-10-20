"""Fibonacci numbers via the fast doubling recurrence.

Fast doubling evaluates a pair of Fibonacci numbers per bit of the index and
yields fib(n) in O(log n) multiplications with no memoisation cache.
"""
import logging

LOG = logging.getLogger(__name__)


def _pair(n):
    """Return the (fib(n), fib(n + 1)) pair using fast doubling."""
    if n == 0:
        return 0, 1
    a, b = _pair(n >> 1)
    c = a * (2 * b - a)
    d = a * a + b * b
    if n & 1:
        return d, c + d
    return c, d


def fibonacci(n):
    """Return the nth Fibonacci number, with fib(0) equal to zero."""
    index = int(n)
    if index < 0:
        raise ValueError('index must be non-negative')
    return _pair(index)[0]


def fibonacci_sequence(count):
    """Return the first count Fibonacci numbers."""
    return [fibonacci(index) for index in range(int(count))]


__all__ = ['fibonacci', 'fibonacci_sequence']
