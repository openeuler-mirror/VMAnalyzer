"""Pause collection when the storage backend falls behind.

Dropping samples silently is worse than delaying them.  This gate tracks
write latency and queue depth, allowing the collection loop to slow down
before the backend becomes unrecoverable.
"""

import logging
import time

LOG = logging.getLogger(__name__)


class BackpressureGate:
    """Track queue depth and latency to decide whether to pause."""

    def __init__(self, depth_limit=5000, latency_limit=2.0):
        if depth_limit <= 0 or latency_limit <= 0:
            raise ValueError("limits must be positive")
        self.depth_limit = depth_limit
        self.latency_limit = latency_limit
        self._paused = False
        self.pauses = 0

    def observe(self, depth, latency):
        """Update the gate state from current backend metrics."""
        should_pause = depth >= self.depth_limit or latency >= self.latency_limit
        if should_pause and not self._paused:
            self.pauses += 1
            LOG.warning("backpressure engaged at depth %d latency %.2fs", depth, latency)
        elif not should_pause and self._paused:
            LOG.info("backpressure released")
        self._paused = should_pause
        return self._paused

    def wait(self, sleep=1.0, timeout=30.0):
        """Block until the gate opens or the timeout elapses."""
        waited = 0.0
        while self._paused and waited < timeout:
            time.sleep(min(sleep, timeout - waited))
            waited += sleep
        if self._paused:
            LOG.warning("backpressure persisted for %.1fs", waited)
        return not self._paused

    @property
    def paused(self):
        """Return whether the gate currently blocks writes."""
        return self._paused
