"""Hysteresis helper that keeps threshold alerts from flapping.

A single crossing is noisy; requiring the metric to fall below a second, lower
threshold before re-arming prevents alert oscillation around the boundary.
"""
import logging

LOG = logging.getLogger(__name__)


class Hysteresis:
    """Two level threshold gate that arms and clears on separate limits."""

    def __init__(self, high, low):
        if low >= high:
            raise ValueError('low threshold must be below the high threshold')
        self.high = float(high)
        self.low = float(low)
        self.active = False

    def update(self, value):
        """Return the new state and whether it changed on this sample."""
        value = float(value)
        previous = self.active
        if not self.active and value >= self.high:
            self.active = True
        elif self.active and value <= self.low:
            self.active = False
        if previous != self.active:
            LOG.debug('hysteresis state %s -> %s', previous, self.active)
        return self.active, self.active != previous


def count_transitions(values, high, low):
    """Return how many times a series toggles the hysteresis gate."""
    gate = Hysteresis(high, low)
    changes = 0
    for value in values or []:
        _state, flipped = gate.update(value)
        if flipped:
            changes += 1
    return changes


__all__ = ['Hysteresis', 'count_transitions']
