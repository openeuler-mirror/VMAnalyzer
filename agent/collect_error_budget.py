#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Error budget accounting for collection cycles.

Operators get an early warning when failures eat a large share of the
allowed budget before the reporting window closes.
"""

import logging
import time

LOG = logging.getLogger(__name__)


class ErrorBudget:
    """Track failures within a sliding window expressed in seconds."""

    def __init__(self, window=300.0, budget=10, clock=time.monotonic):
        self.window = float(window)
        self.budget = int(budget)
        self.clock = clock
        self._failures = []

    def _evict(self, now):
        cutoff = now - self.window
        while self._failures and self._failures[0] < cutoff:
            self._failures.pop(0)

    def record_failure(self):
        """Count one failure and return the remaining budget."""
        now = self.clock()
        self._failures.append(now)
        self._evict(now)
        LOG.debug("failure recorded, %d left in budget", self.remaining())
        return self.remaining()

    def remaining(self):
        """Failures still allowed inside the current window."""
        self._evict(self.clock())
        return max(0, self.budget - len(self._failures))

    def exhausted(self):
        """True when the budget has been fully consumed."""
        return self.remaining() == 0

    def failure_rate(self):
        """Fraction of the budget that has been consumed."""
        if self.budget <= 0:
            return 1.0
        return min(1.0, len(self._failures) / float(self.budget))
