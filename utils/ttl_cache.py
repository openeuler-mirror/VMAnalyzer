"""Time to live cache for slowly changing guest attributes.

Some attributes only need refreshing every few minutes, so a TTL cache avoids
repeated collection while still guaranteeing that data is not stale.
"""
import time
import logging

LOG = logging.getLogger(__name__)


class TtlCache:
    """Cache whose entries expire after a fixed number of seconds."""

    def __init__(self, ttl_seconds):
        if ttl_seconds <= 0:
            raise ValueError('ttl must be positive')
        self.ttl = float(ttl_seconds)
        self.store = {}

    def get(self, key, now=None):
        """Return a live value or None once the entry has expired."""
        entry = self.store.get(key)
        if entry is None:
            return None
        moment = now if now is not None else time.monotonic()
        if moment - entry[1] >= self.ttl:
            del self.store[key]
            LOG.debug('entry %r expired', key)
            return None
        return entry[0]

    def put(self, key, value, now=None):
        """Store a value stamped with the current instant."""
        moment = now if now is not None else time.monotonic()
        self.store[key] = (value, moment)

    def evict_expired(self, now=None):
        """Drop every expired entry and report how many were removed."""
        moment = now if now is not None else time.monotonic()
        stale = [key for key, entry in self.store.items() if moment - entry[1] >= self.ttl]
        for key in stale:
            del self.store[key]
        return len(stale)


__all__ = ['TtlCache']
