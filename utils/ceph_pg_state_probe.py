"""Ceph placement group state audit.

Only active+clean PGs are fully healthy; listing PGs in any other state
focuses recovery work.
"""
import logging

LOG = logging.getLogger(__name__)


def clean_fraction(pgs):
    """Return the fraction of PGs in active+clean state."""
    states = [pg.get('state', '') for pg in pgs or []]
    if not states:
        return 0.0
    clean = sum(1 for s in states if s == 'active+clean')
    return round(clean / float(len(states)), 4)


def unclean_pgs(pgs, limit=20):
    """Return PG ids not in active+clean state."""
    bad = [pg.get('pgid') for pg in pgs or [] if pg.get('state') != 'active+clean']
    LOG.debug('unclean pgs %d', len(bad))
    return bad[:limit]


__all__ = ['clean_fraction', 'unclean_pgs']
