"""Segment tree build cost.

Range-sum queries over metric windows build a segment tree once; the node
count and build comparisons are derived from the window size.
"""
import logging
import math

LOG = logging.getLogger(__name__)


def node_count(window_size):
    """Return the array size needed by a segment tree."""
    n = max(1, int(window_size or 1))
    return 2 * (1 << int(math.ceil(math.log(n, 2)))) - 1


def build_comparisons(window_size):
    """Return comparisons to build the tree over the window."""
    return max(0, node_count(window_size) // 2)


__all__ = ['node_count', 'build_comparisons']
