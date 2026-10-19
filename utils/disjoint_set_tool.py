"""Disjoint set union accounting.

Union-by-rank with path compression keeps operations near-constant; the rank
bound is computed for the element count.
"""
import logging
import math

LOG = logging.getLogger(__name__)


def max_rank(element_count):
    """Return the maximum rank any root can reach."""
    n = max(1, int(element_count or 1))
    return int(math.ceil(math.log(n, 2)))


def compression_passes(parents):
    """Count nodes whose parent is not the root, needing compression."""
    count = sum(1 for node, par in (parents or {}).items() if par != parents.get(par, par))
    LOG.debug('%d nodes need path compression', count)
    return count


__all__ = ['max_rank', 'compression_passes']
