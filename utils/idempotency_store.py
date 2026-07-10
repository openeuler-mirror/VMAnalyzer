#!/usr/bin/env python3
"""Idempotency store for safe operation retries."""
from typing import Any, Optional, Dict, Callable
import hashlib
import time
import threading
from enum import Enum

class IdempotencyStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class IdempotencyRecord:
    def __init__(self, key: str, status: IdempotencyStatus = IdempotencyStatus.PENDING):
        self._key = key
        self._status = status
        self._result: Any = None
        self._error: Optional[str] = None
        self._created = time.time()
        self._updated = time.time()
        self._expires_at = self._created + 86400

    @property
    def key(self) -> str:
        return self._key

    @property
    def status(self) -> IdempotencyStatus:
        return self._status

    @property
    def result(self) -> Any:
        return self._result

    @property
    def error(self) -> Optional[str]:
        return self._error

    @property
    def expired(self) -> bool:
        return time.time() > self._expires_at

    def set_result(self, result: Any) -> None:
        self._result = result
        self._status = IdempotencyStatus.COMPLETED
        self._updated = time.time()

    def set_error(self, error: str) -> None:
        self._error = error
        self._status = IdempotencyStatus.FAILED
        self._updated = time.time()

    def set_pending(self) -> None:
        self._status = IdempotencyStatus.PENDING
        self._updated = time.time()

class IdempotencyStore:
    def __init__(self, ttl: float = 86400, max_keys: int = 100000):
        self._store: Dict[str, IdempotencyRecord] = {}
        self._ttl = ttl
        self._max_keys = max_keys
        self._lock = threading.Lock()
        self._stats = {"hits": 0, "misses": 0, "stored": 0, "evicted": 0}

    def _make_key(self, key: str) -> str:
        return hashlib.sha256(key.encode()).hexdigest()

    def get_or_create(self, key: str) -> tuple:
        hashed = self._make_key(key)
        with self._lock:
            self._evict_expired()
            if hashed in self._store:
                record = self._store[hashed]
                if not record.expired:
                    self._stats["hits"] += 1
                    return record, True
            record = IdempotencyRecord(hashed)
            record._expires_at = time.time() + self._ttl
            self._store[hashed] = record
            self._stats["misses"] += 1
            self._stats["stored"] += 1
            if len(self._store) > self._max_keys:
                self._evict_oldest()
            return record, False

    def execute(self, key: str, func: Callable, *args, **kwargs) -> Any:
        record, exists = self.get_or_create(key)
        if exists:
            if record.status == IdempotencyStatus.COMPLETED:
                return record.result
            elif record.status == IdempotencyStatus.FAILED:
                record.set_pending()
            elif record.status == IdempotencyStatus.PENDING:
                raise RuntimeError("Operation in progress")
        try:
            result = func(*args, **kwargs)
            record.set_result(result)
            return result
        except Exception as e:
            record.set_error(str(e))
            raise

    def get(self, key: str) -> Optional[IdempotencyRecord]:
        hashed = self._make_key(key)
        with self._lock:
            record = self._store.get(hashed)
            if record and record.expired:
                del self._store[hashed]
                self._stats["evicted"] += 1
                return None
            return record

    def remove(self, key: str) -> bool:
        hashed = self._make_key(key)
        with self._lock:
            if hashed in self._store:
                del self._store[hashed]
                return True
            return False

    def _evict_expired(self) -> None:
        expired = [k for k, v in self._store.items() if v.expired]
        for k in expired:
            del self._store[k]
            self._stats["evicted"] += 1

    def _evict_oldest(self) -> None:
        if not self._store:
            return
        oldest = min(self._store.values(), key=lambda r: r._updated)
        del self._store[oldest.key]
        self._stats["evicted"] += 1

    @property
    def stats(self) -> Dict[str, int]:
        with self._lock:
            return dict(self._stats)

    @property
    def size(self) -> int:
        with self._lock:
            return len(self._store)

    def clear(self) -> None:
        with self._lock:
            self._store.clear()

    def set_ttl(self, ttl: float) -> None:
        self._ttl = ttl
