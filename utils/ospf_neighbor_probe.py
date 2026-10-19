"""OSPF neighbour state audit.

Neighbours stuck in EXSTART or TWO-WAY never exchange routes; the audit lists
neighbours that are not FULL.
"""
import logging

LOG = logging.getLogger(__name__)

FULL = 'FULL'


def stuck_neighbors(states):
    """Return {neighbor: state} entries whose state is not FULL."""
    stuck = {n: s for n, s in (states or {}).items() if str(s).upper() != FULL}
    LOG.debug('%d ospf neighbours not full', len(stuck))
    return stuck


def full_ratio(states):
    """Return the share of neighbours in FULL state."""
    if not states:
        return 1.0
    full = sum(1 for s in states.values() if str(s).upper() == FULL)
    return round(full / float(len(states)), 3)


__all__ = ['stuck_neighbors', 'full_ratio']
