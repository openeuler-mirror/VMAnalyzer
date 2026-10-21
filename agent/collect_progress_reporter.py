#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Report collection progress without flooding the log."""

import logging

LOG = logging.getLogger(__name__)


class ProgressReporter:
    """Emit a log line whenever the completion percentage crosses a step."""

    def __init__(self, total, step=10, label="collection", logger=None):
        self.total = max(0, int(total))
        self.step = max(1, int(step))
        self.label = label
        self.logger = logger or LOG
        self.done = 0
        self._last_mark = 0

    def advance(self, count=1):
        """Record completed work and log threshold crossings."""
        self.done = min(self.total, self.done + max(0, int(count)))
        percent = self.percent()
        mark = percent - percent % self.step
        if mark > self._last_mark:
            self._last_mark = mark
            self.logger.info(
                "%s progress: %d%% (%d/%d)", self.label, mark, self.done, self.total
            )
        return percent

    def percent(self):
        """Completion percentage clamped to 0..100."""
        if self.total <= 0:
            return 100.0
        return min(100.0, 100.0 * self.done / self.total)
