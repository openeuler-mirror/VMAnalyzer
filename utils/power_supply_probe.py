"""Power supply wattage headroom.

PSUs run hottest near capacity; drawn watts over rated watts is the headroom
indicator for the BMC report.
"""
import logging

LOG = logging.getLogger(__name__)


def load_ratio(drawn_w, rated_w):
    """Return drawn/rated watts in 0..1."""
    if not rated_w or rated_w <= 0:
        return 0.0
    return round(min(1.0, float(drawn_w or 0) / float(rated_w)), 3)


def oversubscribed(drawn_w, rated_w, ceiling=0.85):
    """Report when the draw crossed the planning ceiling."""
    over = load_ratio(drawn_w, rated_w) >= ceiling
    if over:
        LOG.warning('psu %.0fW of %.0fW', drawn_w, rated_w)
    return over


__all__ = ['load_ratio', 'oversubscribed']
