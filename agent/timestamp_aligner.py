"""Align sample timestamps to a common collection instant.

Probes finish at slightly different times, so samples from one round look
out of order in storage.  Recording the round start as their common
timestamp makes cross-metric joins exact.
"""

import logging

LOG = logging.getLogger(__name__)


class TimestampAligner:
    """Rewrite sample timestamps to a round-level instant."""

    def __init__(self, tolerance=2.0):
        if tolerance < 0:
            raise ValueError("tolerance must not be negative")
        self.tolerance = tolerance
        self.adjusted = 0

    def align(self, round_start, samples):
        """Return samples with timestamps set to the round start."""
        aligned = []
        for sample in samples:
            updated = dict(sample)
            original = float(updated.get("timestamp", round_start))
            if abs(original - round_start) <= self.tolerance:
                updated["timestamp"] = float(round_start)
                self.adjusted += 1
            aligned.append(updated)
        LOG.debug("aligned %d sample timestamp(s) to %.3f", self.adjusted, round_start)
        return aligned

    def within_tolerance(self, timestamp, round_start):
        """Return True when a sample belongs to the current round."""
        return abs(float(timestamp) - float(round_start)) <= self.tolerance
