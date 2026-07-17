#!/usr/bin/env python3
"""Cache invalidation strategy manager with TTL and pattern-based eviction."""
import time
import re
import threading
from typing import Dict, List, Optional, Any

class CacheInvalidator:
    """Manages cache entries with TTL expiration and pattern-based invalidation."""

    def __init__(self):
        self._entries: Dict[str, tuple] = {}
        self._lock = threading.Lock()

    def add(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """Add a cache entry with optional TTL in seconds."""
        expiry = time.time() + ttl if ttl else None
        with self._lock:
            self._entries[key] = (value, expiry)

    def get(self, key: str) -> Optional[Any]:
        """Retrieve a cache entry if not expired."""
        with self._lock:
            if key not in self._entries:
                return None
            value, expiry = self._entries[key]
            if expiry and time.time() > expiry:
                del self._entries[key]
                return None
            return value

    def invalidate(self, key: str) -> bool:
        """Remove a specific cache entry."""
        with self._lock:
            if key in self._entries:
                del self._entries[key]
                return True
            return False

    def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate all entries matching a regex pattern."""
        compiled = re.compile(pattern)
        count = 0
        with self._lock:
            keys_to_remove = [k for k in self._entries if compiled.search(k)]
            for key in keys_to_remove:
                del self._entries[key]
                count += 1
        return count

    def cleanup_expired(self) -> int:
        """Remove all expired entries and return count."""
        now = time.time()
        count = 0
        with self._lock:
            keys_to_remove = [
                k for k, (_, expiry) in self._entries.items()
                if expiry and now > expiry
            ]
            for key in keys_to_remove:
                del self._entries[key]
                count += 1
        return count

    def size(self) -> int:
        """Return current number of valid entries."""
        self.cleanup_expired()
        with self._lock:
            return len(self._entries)

    def keys(self) -> List[str]:
        """Return list of all valid cache keys."""
        self.cleanup_expired()
        with self._lock:
            return list(self._entries.keys())
