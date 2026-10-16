"""Least recently used cache for expensive lookups.

Guest metadata is fetched repeatedly during a scan, so an LRU map keeps the hot
subset resident in memory and bounds growth for long running agents.
"""
from collections import OrderedDict
import logging

LOG = logging.getLogger(__name__)


class LruCache:
    """Ordered dictionary backed cache evicting the least recently used key."""

    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError('capacity must be positive')
        self.capacity = capacity
        self.entries = OrderedDict()

    def get(self, key, default=None):
        """Return a cached value and mark the key as recently used."""
        if key not in self.entries:
            return default
        self.entries.move_to_end(key)
        return self.entries[key]

    def put(self, key, value):
        """Store a value, evicting the oldest entry once the cache is full."""
        self.entries[key] = value
        self.entries.move_to_end(key)
        while len(self.entries) > self.capacity:
            evicted, _ = self.entries.popitem(last=False)
            LOG.debug('evicted key %r', evicted)

    def hit_ratio(self, hits, misses):
        """Return the cache hit ratio for the supplied counters."""
        total = hits + misses
        return round(hits / float(total), 4) if total else 0.0


__all__ = ['LruCache']
