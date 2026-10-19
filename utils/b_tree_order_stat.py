"""B-tree order statistics.

Range scans walk leaves, so estimating the leaf count from keys and order
predicts scan page reads.
"""
import logging
import math

LOG = logging.getLogger(__name__)


def leaf_pages(key_count, order):
    """Return the expected leaf page count for key_count keys."""
    o = max(2, int(order or 2))
    n = max(0, int(key_count or 0))
    leaves = int(math.ceil(n / float(o))) if n else 0
    LOG.debug('b-tree %d keys -> %d leaves', n, leaves)
    return leaves


def height(key_count, order):
    """Return the expected tree height."""
    o = max(2, int(order or 2))
    n = max(1, int(key_count or 1))
    return int(math.ceil(math.log(n, o)))


__all__ = ['leaf_pages', 'height']
