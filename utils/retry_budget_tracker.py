"""Retry budget tracking across a rolling time window.

Unbounded retries can amplify an outage, so the agent caps the number of
retries it will spend in a window and surfaces when the budget is exhausted.
"""
import logging

LOG = logging.getLogger(__name__)


class RetryBudget:
    """Sliding window counter that refuses retries beyond a fixed budget."""

    def __init__(self, budget, window_sec):
        if budget <= 0 or window_sec <= 0:
            raise ValueError('budget and window must be positive')
        self.budget = int(budget)
        self.window = float(window_sec)
        self.events = []

    def _prune(self, now):
        cutoff = float(now) - self.window
        self.events = [stamp for stamp in self.events if stamp >= cutoff]

    def spend(self, now):
        """Record a retry when budget remains and report whether it may run."""
        self._prune(now)
        if len(self.events) >= self.budget:
            LOG.debug('retry budget exhausted')
            return False
        self.events.append(float(now))
        return True

    def remaining(self, now):
        """Return the number of retries still available in the window."""
        self._prune(now)
        return max(0, self.budget - len(self.events))


__all__ = ['RetryBudget']
