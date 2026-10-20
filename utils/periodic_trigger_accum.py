"""Accumulate ticks toward a periodic trigger.

Counts fine grained ticks and fires once every interval worth of ticks, which
avoids drift when no wall clock is available.
"""
from dataclasses import dataclass


@dataclass
class PeriodicAccumulator:
    """Count ticks and emit a fire signal at each interval boundary."""

    interval_ticks: int
    count: int = 0

    def tick(self):
        """Advance one tick and report whether the period elapsed."""
        if self.interval_ticks <= 0:
            raise ValueError("interval_ticks must be positive")
        self.count += 1
        if self.count >= self.interval_ticks:
            self.count -= self.interval_ticks
            return True
        return False

    def progress(self):
        """Return the fraction of the current period already elapsed."""
        if self.interval_ticks <= 0:
            return 0.0
        return round(self.count / float(self.interval_ticks), 4)


__all__ = ["PeriodicAccumulator"]
