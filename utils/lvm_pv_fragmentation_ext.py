"""LVM physical volume fragmentation estimate.

Free extents scattered in small runs cannot back a large new logical volume,
so the largest free run is compared to total free space.
"""
import logging

LOG = logging.getLogger(__name__)


def fragmentation(free_runs):
    """Return 0..1 fragmentation from a list of free extent run sizes."""
    runs = [int(r) for r in free_runs or [] if r and r > 0]
    if not runs:
        return 0.0
    total = sum(runs)
    largest = max(runs)
    return round(1.0 - float(largest) / float(total), 3)


def can_allocate(free_runs, extents_needed):
    """Report whether some free run can hold the requested extents."""
    ok = any(int(r) >= extents_needed for r in free_runs or [] if r)
    LOG.debug('lvm alloc %s extents ok=%s', extents_needed, ok)
    return ok


__all__ = ['fragmentation', 'can_allocate']
