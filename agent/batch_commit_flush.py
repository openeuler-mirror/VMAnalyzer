#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Batch commit helper that flushes buffered samples by size or age."""

import logging
import time

LOG = logging.getLogger(__name__)


class BatchCommitter:
    """Buffer samples and release them when a size or age threshold is hit."""

    def __init__(self, sink, max_items=64, max_age=5.0, clock=time.monotonic):
        if max_items <= 0:
            raise ValueError("max_items must be positive")
        self.sink = sink
        self.max_items = int(max_items)
        self.max_age = float(max_age)
        self.clock = clock
        self._items = []
        self._opened_at = clock()

    def add(self, item):
        """Append one sample, returning the flushed batch when a limit trips."""
        if not self._items:
            self._opened_at = self.clock()
        self._items.append(item)
        if self.should_flush():
            return self.flush()
        return None

    def should_flush(self):
        """True when the item count or buffer age reached its threshold."""
        return len(self._items) >= self.max_items or (
            self.clock() - self._opened_at >= self.max_age
        )

    def flush(self):
        """Forward the buffered samples to the sink and clear the buffer."""
        if not self._items:
            return 0
        batch, self._items = self._items, []
        self._opened_at = self.clock()
        self.sink(batch)
        LOG.debug("flushed %d samples", len(batch))
        return len(batch)
