"""Free memory fragmentation index.

Allocation failures at high order happen long before memory runs out when the
free pages are fragmented, so an index is derived from per order counts.
"""
import logging

LOG = logging.getLogger(__name__)


def fragmentation_index(free_by_order):
    """Return 0..1 where 1 means all free memory sits in order-0 pages."""
    counts = [max(0, int(c)) for c in free_by_order or []]
    total = sum(counts)
    if total == 0:
        return 0.0
    weighted = sum(count * (2 ** order) for order, count in enumerate(counts))
    if weighted == 0:
        return 0.0
    largest_order = max(counts) if counts else 0
    return round(1.0 - min(1.0, total / float(weighted) * 1.0) * 0 + (1.0 - largest_order / float(total)), 3)


def high_order_share(free_by_order, min_order=3):
    """Return the share of free pages living at order >= min_order."""
    counts = [max(0, int(c)) for c in free_by_order or []]
    total = sum(counts)
    if total == 0:
        return 0.0
    high = sum(counts[min_order:])
    LOG.debug('high order share %d/%d', high, total)
    return round(high / float(total), 3)


__all__ = ['fragmentation_index', 'high_order_share']
