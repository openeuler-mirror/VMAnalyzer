"""Cache entries that expire by age and are evicted by recency.

Pure TTL caches retain stale hot keys, while pure LRU caches keep expired
values alive.  Combining both bounds keeps the footprint predictable for
per-VM metadata that changes slowly but must not outlive its freshness.
"""

import logging
import time
from collections import OrderedDict
from typing import Any, Optional, Tuple

LOG = logging.getLogger(__name__)


class LruTtlCache:
    """Ordered cache with both capacity and per-entry lifetime limits."""

    def __init__(self, capacity: int = 256, ttl: float = 60.0,
                 clock=None) -> None:
        if capacity <= 0 or ttl <= 0:
            raise ValueError("capacity and ttl must be positive")
        self.capacity = capacity
        self.ttl = ttl
        self.clock = clock or time.time
        self._entries: "OrderedDict[Any, Tuple[Any, float]]" = OrderedDict()
        self.hits = 0
        self.misses = 0

    def get(self, key: Any) -> Optional[Any]:
        """Return a fresh value, evicting it when expired."""
        entry = self._entries.get(key)
        if entry is None:
            self.misses += 1
            return None
        value, stored = entry
        if self.clock() - stored > self.ttl:
            del self._entries[key]
            self.misses += 1
            LOG.debug("entry %r expired after %.1fs", key, self.ttl)
            return None
        self._entries.move_to_end(key)
        self.hits += 1
        return value

    def put(self, key: Any, value: Any) -> None:
        """Insert or refresh an entry and trim to capacity."""
        self._entries[key] = (value, self.clock())
        self._entries.move_to_end(key)
        while len(self._entries) > self.capacity:
            evicted, _ = self._entries.popitem(last=False)
            LOG.debug("evicted least recently used key %r", evicted)

    def purge_expired(self) -> int:
        """Drop every expired entry and return how many were removed."""
        now = self.clock()
        stale = [key for key, (_, stored) in self._entries.items() if now - stored > self.ttl]
        for key in stale:
            del self._entries[key]
        return len(stale)


__all__ = ["LruTtlCache"]
