#!/usr/bin/env python3
"""Deduplication cache using content-based addressing."""
from typing import Any, Optional, Dict, List, Set
import hashlib
import time
import threading
from collections import OrderedDict

class DedupCache:
    def __init__(self, max_size: int = 10000, ttl: float = 3600):
        self._cache: Dict[str, dict] = {}
        self._max_size = max_size
        self._ttl = ttl
        self._lock = threading.Lock()
        self._stats = {"hits": 0, "misses": 0, "stored": 0, "evicted": 0, "deduped": 0}
        self._access_order: OrderedDict = OrderedDict()

    def _hash(self, content: Any) -> str:
        if isinstance(content, str):
            data = content.encode()
        elif isinstance(content, (bytes, bytearray)):
            data = bytes(content)
        else:
            data = repr(content).encode()
        return hashlib.sha256(data).hexdigest()

    def get_or_store(self, content: Any) -> tuple:
        key = self._hash(content)
        with self._lock:
            self._evict_expired()
            if key in self._cache:
                entry = self._cache[key]
                entry["access_count"] += 1
                entry["last_access"] = time.time()
                self._access_order.move_to_end(key)
                self._stats["hits"] += 1
                self._stats["deduped"] += 1
                return entry["content"], True
            if len(self._cache) >= self._max_size:
                self._evict_lru()
            entry = {
                "content": content,
                "created": time.time(),
                "last_access": time.time(),
                "access_count": 1,
                "size": len(str(content)),
            }
            self._cache[key] = entry
            self._access_order[key] = True
            self._stats["stored"] += 1
            self._stats["misses"] += 1
            return content, False

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            entry = self._cache.get(key)
            if entry is None:
                return None
            if time.time() - entry["created"] > self._ttl:
                del self._cache[key]
                self._access_order.pop(key, None)
                self._stats["evicted"] += 1
                return None
            entry["access_count"] += 1
            entry["last_access"] = time.time()
            self._access_order.move_to_end(key)
            self._stats["hits"] += 1
            return entry["content"]

    def has(self, content: Any) -> bool:
        key = self._hash(content)
        with self._lock:
            return key in self._cache

    def remove(self, content: Any) -> bool:
        key = self._hash(content)
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                self._access_order.pop(key, None)
                return True
            return False

    def _evict_expired(self) -> None:
        now = time.time()
        expired = [k for k, v in self._cache.items() if now - v["created"] > self._ttl]
        for k in expired:
            del self._cache[k]
            self._access_order.pop(k, None)
            self._stats["evicted"] += 1

    def _evict_lru(self) -> None:
        if self._access_order:
            key = next(iter(self._access_order))
            del self._cache[key]
            self._access_order.pop(key, None)
            self._stats["evicted"] += 1

    @property
    def stats(self) -> Dict[str, int]:
        with self._lock:
            return dict(self._stats)

    @property
    def size(self) -> int:
        with self._lock:
            return len(self._cache)

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()
            self._access_order.clear()

    def total_size_bytes(self) -> int:
        with self._lock:
            return sum(e["size"] for e in self._cache.values())

    def dedup_ratio(self) -> float:
        with self._lock:
            total = self._stats["hits"] + self._stats["misses"]
            return self._stats["hits"] / total if total > 0 else 0.0
