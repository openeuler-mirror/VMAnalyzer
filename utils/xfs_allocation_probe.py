"""XFS allocation group free-space balance.

Free space concentrated in a single allocation group forces contention on its
lock, so the spread across groups is measured.
"""
import logging

LOG = logging.getLogger(__name__)


def balance_ratio(group_free_bytes):
    """Return min/max free-space ratio across allocation groups."""
    vals = [float(v) for v in group_free_bytes or [] if v is not None and v >= 0]
    if not vals:
        return 0.0
    hi = max(vals)
    if hi <= 0:
        return 0.0
    return round(min(vals) / hi, 3)


def needs_rebalance(ratio, floor=0.2):
    """Report when the balance ratio fell below the floor."""
    bad = ratio < floor
    if bad:
        LOG.warning('xfs AG imbalance ratio=%.3f', ratio)
    return bad


__all__ = ['balance_ratio', 'needs_rebalance']
