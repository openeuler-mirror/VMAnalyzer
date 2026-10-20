"""Dentry cache pressure estimate.

A ballooning dentry cache squeezes page cache, so dentries are compared to a
share of total memory pages.
"""
import logging

LOG = logging.getLogger(__name__)


def dentry_share(dentries, total_pages):
    """Return dentries per total memory page."""
    if not total_pages or total_pages <= 0:
        return 0.0
    return round(float(dentries or 0) / float(total_pages), 4)


def reclaim_advised(share, ceiling=0.5):
    """Report when dentries crowd out page cache."""
    advise = share >= ceiling
    if advise:
        LOG.warning('dentry share %.3f, advise reclaim', share)
    return advise


__all__ = ['dentry_share', 'reclaim_advised']
