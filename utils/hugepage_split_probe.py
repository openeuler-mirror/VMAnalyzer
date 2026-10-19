"""Transparent hugepage split event tracking.

Frequent splits defeat the purpose of THP; counting split events relative to
faults shows whether the workload actually benefits.
"""
import logging

LOG = logging.getLogger(__name__)


def split_ratio(splits, faults):
    """Return splits per hugepage fault."""
    if not faults or faults <= 0:
        return 0.0
    return round(float(splits) / float(faults), 3)


def is_thrashing(splits, faults, watermark=0.5):
    """Report when splits exceed the share of faults considered healthy."""
    ratio = split_ratio(splits, faults)
    if ratio >= watermark:
        LOG.debug('thp thrashing ratio %.3f', ratio)
        return True
    return False


__all__ = ['split_ratio', 'is_thrashing']
