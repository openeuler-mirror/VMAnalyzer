#!/usr/bin/env python3
"""Token bucket rate limiter for traffic control."""
from typing import Dict, Optional
import time
import threading

class TokenBucket:
    def __init__(self, capacity: float, refill_rate: float):
        self._capacity = capacity
        self._refill_rate = refill_rate
        self._tokens = capacity
        self._last_refill = time.monotonic()
        self._lock = threading.Lock()

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(self._capacity, self._tokens + elapsed * self._refill_rate)
        self._last_refill = now

    def consume(self, tokens: float = 1.0) -> bool:
        with self._lock:
            self._refill()
            if self._tokens >= tokens:
                self._tokens -= tokens
                return True
            return False

    def wait_for_token(self, tokens: float = 1.0, timeout: float = 60.0) -> bool:
        start = time.monotonic()
        while time.monotonic() - start < timeout:
            if self.consume(tokens):
                return True
            time.sleep(0.01)
        return False

    @property
    def tokens(self) -> float:
        with self._lock:
            self._refill()
            return self._tokens

    @property
    def capacity(self) -> float:
        return self._capacity

class RateLimiter:
    def __init__(self, default_rate: float = 10.0):
        self._buckets: Dict[str, TokenBucket] = {}
        self._default_rate = default_rate

    def get_bucket(self, key: str, rate: Optional[float] = None) -> TokenBucket:
        if key not in self._buckets:
            r = rate or self._default_rate
            self._buckets[key] = TokenBucket(capacity=r * 2, refill_rate=r)
        return self._buckets[key]

    def allow(self, key: str = "default") -> bool:
        return self.get_bucket(key).consume()

    def set_rate(self, key: str, rate: float) -> None:
        self._buckets[key] = TokenBucket(capacity=rate * 2, refill_rate=rate)

    def reset(self, key: Optional[str] = None) -> None:
        if key:
            self._buckets.pop(key, None)
        else:
            self._buckets.clear()

    def keys(self) -> list:
        return list(self._buckets.keys())
