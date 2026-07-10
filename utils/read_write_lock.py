#!/usr/bin/env python3
"""Read-write lock for concurrent read access with exclusive writes."""
from typing import Optional
import threading

class ReadWriteLock:
    def __init__(self):
        self._readers = 0
        self._writers_waiting = 0
        self._writer_active = False
        self._lock = threading.Lock()
        self._read_ready = threading.Condition(self._lock)
        self._write_ready = threading.Condition(self._lock)
        self._stats = {"reads": 0, "writes": 0, "read_waits": 0, "write_waits": 0}

    def acquire_read(self, timeout: Optional[float] = None) -> bool:
        start = threading.Event()
        with self._lock:
            while self._writer_active or self._writers_waiting > 0:
                self._stats["read_waits"] += 1
                if not self._read_ready.wait(timeout):
                    return False
            self._readers += 1
            self._stats["reads"] += 1
        return True

    def release_read(self) -> None:
        with self._lock:
            self._readers -= 1
            if self._readers == 0:
                self._write_ready.notify()

    def acquire_write(self, timeout: Optional[float] = None) -> bool:
        with self._lock:
            self._writers_waiting += 1
            while self._readers > 0 or self._writer_active:
                self._stats["write_waits"] += 1
                if not self._write_ready.wait(timeout):
                    self._writers_waiting -= 1
                    return False
            self._writers_waiting -= 1
            self._writer_active = True
            self._stats["writes"] += 1
        return True

    def release_write(self) -> None:
        with self._lock:
            self._writer_active = False
            if self._writers_waiting > 0:
                self._write_ready.notify()
            else:
                self._read_ready.notify_all()

    @property
    def stats(self) -> dict:
        with self._lock:
            return dict(self._stats)

    @property
    def reader_count(self) -> int:
        with self._lock:
            return self._readers

    @property
    def writer_active(self) -> bool:
        with self._lock:
            return self._writer_active

    @property
    def writers_waiting(self) -> int:
        with self._lock:
            return self._writers_waiting

class ReadLockContext:
    def __init__(self, rwlock: ReadWriteLock, timeout: Optional[float] = None):
        self._lock = rwlock
        self._timeout = timeout
        self._acquired = False

    def __enter__(self):
        self._acquired = self._lock.acquire_read(self._timeout)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._acquired:
            self._lock.release_read()
        return False

class WriteLockContext:
    def __init__(self, rwlock: ReadWriteLock, timeout: Optional[float] = None):
        self._lock = rwlock
        self._timeout = timeout
        self._acquired = False

    def __enter__(self):
        self._acquired = self._lock.acquire_write(self._timeout)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._acquired:
            self._lock.release_write()
        return False

class LockedResource:
    def __init__(self, data: any = None):
        self._data = data
        self._lock = ReadWriteLock()

    def read(self, func, *args, **kwargs):
        with ReadLockContext(self._lock):
            return func(self._data, *args, **kwargs)

    def write(self, func, *args, **kwargs):
        with WriteLockContext(self._lock):
            return func(self._data, *args, **kwargs)

    @property
    def lock(self) -> ReadWriteLock:
        return self._lock

    @property
    def stats(self) -> dict:
        return self._lock.stats
