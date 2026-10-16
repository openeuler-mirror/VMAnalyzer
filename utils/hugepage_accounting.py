"""Huge page accounting helpers.

Transparent huge pages change both the effective memory footprint and the
observable minor fault rate.  These helpers separate hugetlbfs reservations
from anonymous THP usage so leak reports are not misread.
"""
import logging

LOG = logging.getLogger(__name__)

PAGE_SIZE_KB = 4
HUGE_PAGE_KB = 2048


def to_huge_pages(size_kb, huge_kb=HUGE_PAGE_KB):
    """Convert a KiB size into the number of huge pages it needs."""
    if huge_kb <= 0:
        raise ValueError('huge_kb must be positive')
    return int(size_kb + huge_kb - 1) // huge_kb


def split_memory(anonymous_kb, hugetlbfs_kb, total_kb):
    """Split guest memory into anonymous, hugetlbfs and other shares."""
    used = anonymous_kb + hugetlbfs_kb
    other = max(0, total_kb - used)
    if total_kb <= 0:
        LOG.warning('total_kb is not positive, ratios set to zero')
        return {'anonymous_ratio': 0.0, 'hugetlbfs_ratio': 0.0, 'other_ratio': 0.0}
    return {
        'anonymous_ratio': round(anonymous_kb / float(total_kb), 4),
        'hugetlbfs_ratio': round(hugetlbfs_kb / float(total_kb), 4),
        'other_ratio': round(other / float(total_kb), 4),
    }


def reservation_shortfall(reserved_pages, free_pages):
    """Return how many reserved huge pages are still unbacked."""
    return max(0, int(reserved_pages) - int(free_pages))


__all__ = ['to_huge_pages', 'split_memory', 'reservation_shortfall']
