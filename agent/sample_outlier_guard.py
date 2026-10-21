"""Reject impossible metric samples before they reach storage.

A single corrupted sample can flatten every chart that includes it.  The
guard compares each sample against the running median and drops values that
exceed a relative tolerance.
"""

import logging
import statistics

LOG = logging.getLogger(__name__)

HISTORY = 9


class OutlierGuard:
    """Track a short history per metric and reject wild values."""

    def __init__(self, tolerance=0.5, minimum_history=5):
        if tolerance <= 0:
            raise ValueError("tolerance must be positive")
        self.tolerance = tolerance
        self.minimum_history = minimum_history
        self._history = {}
        self.rejected = 0

    def check(self, metric, value):
        """Return True when the value is plausible for this metric."""
        try:
            number = float(value)
        except (TypeError, ValueError):
            LOG.warning("non-numeric sample for %s rejected", metric)
            self.rejected += 1
            return False
        history = self._history.setdefault(metric, [])
        if len(history) >= self.minimum_history:
            median = statistics.median(history)
            limit = abs(median) * self.tolerance
            if limit > 0 and abs(number - median) > limit:
                self.rejected += 1
                LOG.info("sample %.3f for %s exceeds tolerance around %.3f",
                         number, metric, median)
                return False
        history.append(number)
        del history[:-HISTORY]
        return True

    def reset(self, metric=None):
        """Clear history for one metric or all metrics."""
        if metric is None:
            self._history.clear()
            return
        self._history.pop(metric, None)
