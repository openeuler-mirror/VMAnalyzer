#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Per-VM locks shared between collection threads."""

import logging
import threading

LOG = logging.getLogger(__name__)


class LockRegistry:
    """Hand out one lock per VM without blocking unrelated VMs."""

    def __init__(self):
        self._lock = threading.Lock()
        self._locks = {}

    def get(self, vm_name):
        """Return the lock for *vm_name*, creating it on first use."""
        with self._lock:
            lock = self._locks.get(vm_name)
            if lock is None:
                lock = threading.Lock()
                self._locks[vm_name] = lock
                LOG.debug("created lock for %s", vm_name)
            return lock

    def release(self, vm_name):
        """Forget a lock once its VM disappears."""
        with self._lock:
            self._locks.pop(vm_name, None)

    def prune(self, active):
        """Drop locks for VMs outside the active set."""
        active = set(active)
        with self._lock:
            stale = [name for name in self._locks if name not in active]
            for name in stale:
                del self._locks[name]
        if stale:
            LOG.debug("pruned %d stale locks", len(stale))
        return stale

    def __len__(self):
        return len(self._locks)
