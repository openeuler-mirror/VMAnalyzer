"""Split a timeout budget across retry attempts.

Divides an overall deadline across attempts so the sum of per-attempt timeouts
never overruns the caller deadline.
"""
import logging

LOG = logging.getLogger(__name__)


def even_split(total_seconds, attempts):
    """Return an equal per-attempt timeout for a number of attempts."""
    if attempts <= 0:
        raise ValueError("attempts must be positive")
    return total_seconds / float(attempts)


def decreasing_split(total_seconds, attempts, factor=0.5):
    """Return a geometrically decreasing per-attempt timeout list."""
    weights = [factor ** i for i in range(max(0, attempts))]
    total_weight = sum(weights) or 1.0
    return [round(total_seconds * w / total_weight, 4) for w in weights]


def remaining_budget(total_seconds, spent_seconds):
    """Return the budget left after some spending, never negative."""
    return max(0.0, total_seconds - spent_seconds)


__all__ = ["even_split", "decreasing_split", "remaining_budget"]
