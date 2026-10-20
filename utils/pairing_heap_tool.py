"""Pairing heap amortised cost.

Pairing heaps win on decrease-key heavy workloads; the amortised bound guides
the choice over a binary heap.
"""
import logging
import math

LOG = logging.getLogger(__name__)


def amortised_decrease_key(node_count):
    """Return the amortised decrease-key bound in comparisons."""
    n = max(2, int(node_count or 2))
    return int(math.ceil(math.log(n, 2) / math.log(math.log(n, 2), 2)) or 1)


def prefer_pairing(decrease_keys, inserts):
    """Report when decrease-key volume favours a pairing heap."""
    prefer = int(decrease_keys or 0) > 2 * int(inserts or 0)
    LOG.debug('pairing preferred=%s', prefer)
    return prefer


__all__ = ['amortised_decrease_key', 'prefer_pairing']
