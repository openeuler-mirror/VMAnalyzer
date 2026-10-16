"""Kernel samepage merging benefit estimation.

KSM de-duplicates identical pages across guests, so the sharing ratio shows how
much memory is genuinely reclaimed versus merely scanned.
"""
import logging

LOG = logging.getLogger(__name__)


def sharing_ratio(shared_pages, merged_pages):
    """Return the share of scanned pages that were merged."""
    scanned = int(merged_pages)
    if scanned <= 0:
        LOG.debug('KSM has not scanned any pages')
        return 0.0
    return round(min(1.0, int(shared_pages) / float(scanned)), 4)


def reclaimed_mb(shared_pages, page_size_kb=4):
    """Return the memory reclaimed by KSM expressed in megabytes."""
    return round(int(shared_pages) * int(page_size_kb) / 1024.0, 3)


def benefit_verdict(ratio, scanning_cost_pct, good=0.2, cost_limit=5.0):
    """Judge whether KSM benefit justifies its scanning cost."""
    if scanning_cost_pct > cost_limit and ratio < good:
        return 'wasteful'
    if ratio >= good:
        return 'beneficial'
    return 'marginal'


__all__ = ['sharing_ratio', 'reclaimed_mb', 'benefit_verdict']
