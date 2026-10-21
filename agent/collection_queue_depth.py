#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Guard against unbounded collection queues."""

import logging

LOG = logging.getLogger(__name__)


class QueueDepthGuard:
    """Reject or drop work when the queue grows past its limit."""

    def __init__(self, limit=1000, policy="drop_oldest"):
        if policy not in ("drop_oldest", "reject"):
            raise ValueError("policy must be drop_oldest or reject")
        self.limit = int(limit)
        self.policy = policy
        self.items = []
        self.dropped = 0

    def offer(self, item):
        """Queue one item and report whether it was accepted."""
        if len(self.items) < self.limit:
            self.items.append(item)
            return True
        self.dropped += 1
        if self.policy == "reject":
            LOG.warning("queue full, rejecting %r", item)
            return False
        self.items.pop(0)
        self.items.append(item)
        LOG.debug("queue full, dropped the oldest item")
        return True

    def depth(self):
        """Number of items currently waiting."""
        return len(self.items)

    def saturation(self):
        """Queue depth as a fraction of the configured limit."""
        if self.limit <= 0:
            return 1.0
        return len(self.items) / float(self.limit)

    def drain(self):
        """Remove and return every queued item."""
        items, self.items = self.items, []
        return items
