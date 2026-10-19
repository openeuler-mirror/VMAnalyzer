"""Treap expected depth.

Randomised treaps balance with high probability; expected depth guides the
priority RNG range choice.
"""
import logging
import math

LOG = logging.getLogger(__name__)


def expected_depth(key_count):
    """Return the expected depth of a random key."""
    n = max(1, int(key_count or 1))
    depth = 2 * math.log(n) if n > 1 else 0.0
    LOG.debug('treap expected depth %.1f', depth)
    return round(depth, 2)


def priority_range(key_count):
    """Return a priority RNG range that keeps collisions rare."""
    n = max(1, int(key_count or 1))
    return n * n


__all__ = ['expected_depth', 'priority_range']
