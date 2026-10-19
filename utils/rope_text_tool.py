"""Rope rebalance threshold.

Text ropes degrade when leaf sizes skew; the depth limit from the rope length
decides when to rebalance.
"""
import logging
import math

LOG = logging.getLogger(__name__)


def depth_limit(text_length):
    """Return the maximum healthy rope depth for the text length."""
    n = max(2, int(text_length or 2))
    return int(2 * math.ceil(math.log(n, 1.618)))


def needs_rebalance(current_depth, text_length):
    """Report when the rope grew deeper than the Fibonacci bound."""
    need = int(current_depth or 0) > depth_limit(text_length)
    LOG.debug('rope depth %s limit %s', current_depth, depth_limit(text_length))
    return need


__all__ = ['depth_limit', 'needs_rebalance']
