"""Leaky bucket drain simulation.

Models a queue that empties at a constant rate so admission control can predict
the backlog depth after a burst.
"""
import logging

LOG = logging.getLogger(__name__)


def drained_depth(depth, drain_rate, elapsed):
    """Return the queue depth after draining for elapsed seconds."""
    if drain_rate < 0:
        raise ValueError("drain_rate must be non negative")
    return max(0.0, depth - max(0.0, elapsed) * drain_rate)


def projected_depth(depth, inflow, drain_rate, elapsed):
    """Return the depth after simultaneous inflow and drain."""
    net = inflow - drain_rate
    return max(0.0, depth + net * max(0.0, elapsed))


def overflow(depth, capacity, inflow, drain_rate, elapsed):
    """Report whether a bucket overflows within the elapsed horizon."""
    return projected_depth(depth, inflow, drain_rate, elapsed) > capacity


__all__ = ["drained_depth", "projected_depth", "overflow"]
