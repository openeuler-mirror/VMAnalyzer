"""NUMA memory balance scoring.

Memory spread unevenly across nodes forces remote accesses; the score compares
each node against the ideal even share.
"""
import logging

LOG = logging.getLogger(__name__)


def balance_score(pages_by_node):
    """Return 0..1 where 1 means perfectly even distribution."""
    pages = [max(0, int(p)) for p in pages_by_node or []]
    total = sum(pages)
    if not pages or total == 0:
        return 0.0
    ideal = total / float(len(pages))
    deviation = sum(abs(p - ideal) for p in pages) / 2.0
    return round(1.0 - deviation / float(total), 3)


def heaviest_node(pages_by_node):
    """Return the index of the node holding the most pages."""
    pages = list(pages_by_node or [])
    if not pages:
        return -1
    LOG.debug('numa pages %s', pages)
    return max(range(len(pages)), key=lambda i: pages[i])


__all__ = ['balance_score', 'heaviest_node']
