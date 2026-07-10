#!/usr/bin/env python3
"""Counting semaphore with permit management."""
from typing import Optional, List, Callable
import threading
import time
from collections import deque

class Semaphore:
    def __init__(self, permits: int = 1, fair: bool = False):
        self._permits = permits
        self._available = permits
        self._fair = fair
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._wait_queue: deque = deque() if fair else None
        self._stats = {"acquired": 0, "released": 0, "timed_out": 0, "waiting": 0}

    def acquire(self, permits: int = 1, timeout: Optional[float] = None) -> bool:
        with self._condition:
            if self._fair:
                ticket = object()
                self._wait_queue.append(ticket)
                while self._wait_queue[0] is not ticket or self._available < permits:
                    self._stats["waiting"] += 1
                    if timeout is None:
                        self._condition.wait()
                    elif not self._condition.wait(timeout):
                        self._wait_queue.remove(ticket)
                        self._stats["timed_out"] += 1
                        return False
                self._wait_queue.popleft()
            else:
                while self._available < permits:
                    self._stats["waiting"] += 1
                    if timeout is None:
                        self._condition.wait()
                    elif not self._condition.wait(timeout):
                        self._stats["timed_out"] += 1
                        return False
            self._available -= permits
            self._stats["acquired"] += 1
            self._condition.notify_all()
            return True

    def release(self, permits: int = 1) -> None:
        with self._condition:
            self._available += permits
            if self._available > self._permits:
                self._available = self._permits
            self._stats["released"] += 1
            self._condition.notify_all()

    def try_acquire(self, permits: int = 1) -> bool:
        with self._condition:
            if self._available >= permits:
                self._available -= permits
                self._stats["acquired"] += 1
                return True
            return False

    def reduce_permits(self, reduction: int) -> None:
        with self._condition:
            self._available = max(0, self._available - reduction)
            self._permits = max(0, self._permits - reduction)

    def increase_permits(self, increase: int) -> None:
        with self._condition:
            self._permits += increase
            self._available += increase
            self._condition.notify_all()

    @property
    def available_permits(self) -> int:
        return self._available

    @property
    def total_permits(self) -> int:
        return self._permits

    @property
    def is_fair(self) -> bool:
        return self._fair

    @property
    def has_queued_threads(self) -> bool:
        return self._fair and len(self._wait_queue) > 0

    @property
    def queue_length(self) -> int:
        return len(self._wait_queue) if self._fair else 0

    @property
    def stats(self) -> dict:
        with self._lock:
            return dict(self._stats)

    def drain_permits(self) -> int:
        with self._condition:
            drained = self._available
            self._available = 0
            return drained

class PermitContext:
    def __init__(self, semaphore: Semaphore, permits: int = 1,
                 timeout: Optional[float] = None):
        self._semaphore = semaphore
        self._permits = permits
        self._timeout = timeout
        self._acquired = False

    def __enter__(self) -> bool:
        self._acquired = self._semaphore.acquire(self._permits, self._timeout)
        return self._acquired

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._acquired:
            self._semaphore.release(self._permits)
            self._acquired = False
        return False

class RateSemaphore:
    def __init__(self, max_concurrent: int = 10, rate_limit: float = 100.0,
                 time_window: float = 1.0):
        self._semaphore = Semaphore(max_concurrent)
        self._rate_limit = rate_limit
        self._time_window = time_window
        self._timestamps: deque = deque()
        self._lock = threading.Lock()

    def acquire(self, timeout: Optional[float] = None) -> bool:
        now = time.time()
        with self._lock:
            cutoff = now - self._time_window
            while self._timestamps and self._timestamps[0] < cutoff:
                self._timestamps.popleft()
            if len(self._timestamps) >= self._rate_limit:
                return False
            self._timestamps.append(now)
        return self._semaphore.acquire(1, timeout)

    def release(self) -> None:
        self._semaphore.release()

    @property
    def available_permits(self) -> int:
        return self._semaphore.available_permits

    @property
    def current_rate(self) -> float:
        now = time.time()
        with self._lock:
            cutoff = now - self._time_window
            count = sum(1 for t in self._timestamps if t >= cutoff)
        return count / self._time_window

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
        return False
