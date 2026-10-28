"""Keep a bounded window of recent msi enable samples.

Dashboards need the latest average and a tail percentile without storing an
unbounded history.  The window keeps insertion order and evicts the oldest
sample once the capacity is reached.
"""

import logging
from collections import deque

LOG = logging.getLogger(__name__)


class RollingMsiEnable:
    """Fixed capacity window with average and percentile helpers."""

    def __init__(self, capacity=120):
        if capacity < 1:
            raise ValueError("capacity must be positive")
        self.capacity = int(capacity)
        self._samples = deque(maxlen=self.capacity)

    def push(self, value):
        """Append a sample and return the current window size."""
        self._samples.append(float(value))
        return len(self._samples)

    def mean(self):
        """Return the arithmetic mean of the window, or None when empty."""
        if not self._samples:
            return None
        return sum(self._samples) / len(self._samples)

    def percentile(self, ratio=0.95):
        """Return the requested percentile using nearest rank selection."""
        if not self._samples:
            return None
        ordered = sorted(self._samples)
        index = int(round((len(ordered) - 1) * float(ratio)))
        return ordered[max(0, min(index, len(ordered) - 1))]

    def reset(self):
        """Drop every stored sample."""
        self._samples.clear()
        LOG.debug("reset msi_enable rolling window")


__all__ = ["RollingMsiEnable"]
