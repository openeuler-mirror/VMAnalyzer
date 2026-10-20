"""Choose a sampling interval for a retention budget.

Balances how many points a retention window keeps against the storage budget by
deriving the coarsest interval that still fits.
"""
import logging

LOG = logging.getLogger(__name__)


def points_for(span_seconds, interval_seconds):
    """Return how many samples fit in a span at a given interval."""
    if interval_seconds <= 0:
        raise ValueError("interval_seconds must be positive")
    return int(span_seconds // interval_seconds) + 1


def interval_for_budget(span_seconds, max_points):
    """Return the smallest interval keeping points within the budget."""
    if max_points <= 1:
        return int(span_seconds)
    return int(span_seconds // (max_points - 1))


def is_within_budget(span_seconds, interval_seconds, max_points):
    """Report whether an interval keeps sampling within the point budget."""
    return points_for(span_seconds, interval_seconds) <= max_points


__all__ = ["points_for", "interval_for_budget", "is_within_budget"]
