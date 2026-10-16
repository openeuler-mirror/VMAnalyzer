"""Transparent huge page efficiency assessment.

Transparent huge pages only help when backed by contiguous physical memory, so
collapse and fallback counters are compared to judge real efficiency.
"""
import logging

LOG = logging.getLogger(__name__)


def collapse_ratio(allocations, collapses):
    """Return the share of huge page allocations that collapsed successfully."""
    total = int(allocations)
    if total <= 0:
        LOG.debug('no huge page allocations observed')
        return 0.0
    return round(min(1.0, int(collapses) / float(total)), 4)


def fallback_share(fallbacks, allocations):
    """Return the share of attempts that fell back to base pages."""
    total = int(allocations) + int(fallbacks)
    if total <= 0:
        return 0.0
    return round(int(fallbacks) / float(total), 4)


def efficiency_verdict(ratio, fallback, good=0.8, bad=0.5):
    """Classify huge page efficiency as good, partial or poor."""
    if ratio >= good and fallback <= 1.0 - good:
        return 'good'
    if ratio < bad:
        return 'poor'
    return 'partial'


__all__ = ['collapse_ratio', 'fallback_share', 'efficiency_verdict']
