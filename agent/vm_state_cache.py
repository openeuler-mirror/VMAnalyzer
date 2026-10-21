#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Time-limited cache for VM runstate lookups.

Repeated virsh queries dominate collection time when many metrics are
gathered per cycle, so a short cache keeps snapshots consistent.
"""

import logging
import time

LOG = logging.getLogger(__name__)


class VMStateCache:
    """Cache runstates for a small TTL window."""

    def __init__(self, ttl=2.0, clock=time.monotonic):
        self.ttl = float(ttl)
        self.clock = clock
        self._entries = {}

    def get(self, vm_name):
        """Return the cached state, or None when missing and stale."""
        entry = self._entries.get(vm_name)
        if entry is None:
            return None
        state, stamped = entry
        if self.clock() - stamped > self.ttl:
            self._entries.pop(vm_name, None)
            LOG.debug("cache entry for %s expired", vm_name)
            return None
        return state

    def put(self, vm_name, state):
        """Store one state value and return it for chaining."""
        self._entries[vm_name] = (state, self.clock())
        return state

    def invalidate(self, vm_name=None):
        """Drop one entry, or every entry when no name is given."""
        if vm_name is None:
            self._entries.clear()
        else:
            self._entries.pop(vm_name, None)

    def __len__(self):
        return len(self._entries)
