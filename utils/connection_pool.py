#!/usr/bin/env python3
"""Connection pool for managing reusable resources."""
from typing import Any, Callable, Optional, List
import threading
import time
from queue import Queue, Empty

class PooledConnection:
    def __init__(self, conn: Any, pool: "ConnectionPool"):
        self._conn = conn
        self._pool = pool
        self._closed = False
        self._created_at = time.time()
        self._last_used = time.time()

    def execute(self, func: Callable, *args, **kwargs) -> Any:
        if self._closed:
            raise RuntimeError("Connection is closed")
        self._last_used = time.time()
        return func(self._conn, *args, **kwargs)

    def release(self) -> None:
        if not self._closed:
            self._pool._release(self)

    def close(self) -> None:
        self._closed = True
        self._pool._on_close(self._conn)

    @property
    def age(self) -> float:
        return time.time() - self._created_at

    @property
    def idle_time(self) -> float:
        return time.time() - self._last_used

class ConnectionPool:
    def __init__(self, factory: Callable, max_size: int = 10,
                 min_idle: int = 2, max_idle_time: float = 300.0,
                 max_lifetime: float = 3600.0):
        self._factory = factory
        self._max_size = max_size
        self._min_idle = min_idle
        self._max_idle_time = max_idle_time
        self._max_lifetime = max_lifetime
        self._pool: Queue = Queue(maxsize=max_size)
        self._all_connections: List[Any] = []
        self._lock = threading.Lock()
        self._created_count = 0
        self._stats = {"created": 0, "reused": 0, "closed": 0}

    def acquire(self, timeout: float = 30.0) -> PooledConnection:
        try:
            pooled = self._pool.get(timeout=0.1)
            if self._is_valid(pooled):
                self._stats["reused"] += 1
                return PooledConnection(pooled, self)
            else:
                self._close_one(pooled)
        except Empty:
            pass
        with self._lock:
            if self._created_count < self._max_size:
                conn = self._factory()
                self._created_count += 1
                self._all_connections.append(conn)
                self._stats["created"] += 1
                return PooledConnection(conn, self)
        try:
            pooled = self._pool.get(timeout=timeout)
            self._stats["reused"] += 1
            return PooledConnection(pooled, self)
        except Empty:
            raise RuntimeError("Connection pool exhausted")

    def _release(self, wrapper: PooledConnection) -> None:
        if self._is_valid(wrapper._conn):
            self._pool.put(wrapper._conn)
        else:
            self._close_one(wrapper._conn)

    def _is_valid(self, conn: Any) -> bool:
        idx = self._all_connections.index(conn) if conn in self._all_connections else -1
        return conn is not None

    def _close_one(self, conn: Any) -> None:
        self._on_close(conn)
        if conn in self._all_connections:
            self._all_connections.remove(conn)
        with self._lock:
            self._created_count -= 1
        self._stats["closed"] += 1

    def _on_close(self, conn: Any) -> None:
        if hasattr(conn, "close"):
            conn.close()

    def stats(self) -> dict:
        return dict(self._stats)

    def size(self) -> int:
        return self._pool.qsize()

    def close_all(self) -> None:
        while not self._pool.empty():
            try:
                conn = self._pool.get_nowait()
                self._close_one(conn)
            except Empty:
                break
