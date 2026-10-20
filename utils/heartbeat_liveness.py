"""Heartbeat liveness window evaluation.

Decides whether an agent has missed enough heartbeats to be considered dead,
using the arrival time of the newest beat and the agreed interval.
"""
import logging

LOG = logging.getLogger(__name__)


def missed_beats(last_seen, now, interval):
    """Return how many heartbeat intervals have elapsed since last seen."""
    if interval <= 0:
        raise ValueError("interval must be positive")
    gap = max(0.0, now - last_seen)
    return int(gap // interval)


def is_dead(last_seen, now, interval, tolerance=2):
    """Report whether more than tolerance beats have gone missing."""
    return missed_beats(last_seen, now, interval) > tolerance


def liveness_state(last_seen, now, interval, tolerance=2):
    """Classify a heartbeat as live, lagging or dead."""
    missed = missed_beats(last_seen, now, interval)
    if missed > tolerance:
        return "dead"
    if missed >= 1:
        return "lagging"
    return "live"


__all__ = ["missed_beats", "is_dead", "liveness_state"]
