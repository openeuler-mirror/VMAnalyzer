"""Suppress duplicate collection results within a short time window.

Retry logic can produce two identical samples for the same VM and second.
Deduplicating them keeps rate calculations honest without changing the
collection schedule.
"""

import logging
import time

LOG = logging.getLogger(__name__)


class DedupWindow:
    """Remember recent fingerprints per VM for a fixed window."""

    def __init__(self, window=5.0, clock=None):
        if window < 0:
            raise ValueError("window must not be negative")
        self.window = window
        self.clock = clock or time.time
        self._seen = {}
        self.suppressed = 0

    def accept(self, vm_name, fingerprint):
        """Return True when the fingerprint has not been seen recently."""
        now = self.clock()
        previous = self._seen.get(vm_name)
        if previous is not None:
            stamp, known = previous
            if known == fingerprint and now - stamp <= self.window:
                self.suppressed += 1
                LOG.debug("suppressed duplicate sample for %s", vm_name)
                return False
        self._seen[vm_name] = (now, fingerprint)
        return True

    def purge(self):
        """Drop entries older than the window and return the count removed."""
        now = self.clock()
        stale = [name for name, (stamp, _) in self._seen.items() if now - stamp > self.window]
        for name in stale:
            del self._seen[name]
        return len(stale)
