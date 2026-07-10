#!/usr/bin/env python3
"""Resource pool for managed resource lifecycle."""
from typing import Any, Callable, Dict, List, Optional, TypeVar, Generic
from abc import ABC, abstractmethod
import threading
import time
from queue import Queue, Empty

T = TypeVar("T")

class Resource(ABC, Generic[T]):
    def __init__(self, value: T):
        self._value = value
        self._in_use = False
        self._created = time.time()
        self._last_used = time.time()
        self._use_count = 0

    @property
    def value(self) -> T:
        return self._value

    @property
    def in_use(self) -> bool:
        return self._in_use

    @property
    def age(self) -> float:
        return time.time() - self._created

    @property
    def idle_time(self) -> float:
        return time.time() - self._last_used

    @property
    def use_count(self) -> int:
        return self._use_count

    def acquire(self) -> T:
        self._in_use = True
        self._use_count += 1
        return self._value

    def release(self) -> None:
        self._in_use = False
        self._last_used = time.time()

    @abstractmethod
    def is_valid(self) -> bool: ...

    @abstractmethod
    def close(self) -> None: ...

class ResourcePool(Generic[T]):
    def __init__(self, factory: Callable[[], Resource[T]], max_size: int = 10,
                 min_idle: int = 1, max_idle_time: float = 300.0,
                 max_lifetime: float = 3600.0):
        self._factory = factory
        self._max_size = max_size
        self._min_idle = min_idle
        self._max_idle_time = max_idle_time
        self._max_lifetime = max_lifetime
        self._idle: Queue = Queue(maxsize=max_size)
        self._all: List[Resource[T]] = []
        self._lock = threading.Lock()
        self._stats = {"created": 0, "acquired": 0, "released": 0,
                      "destroyed": 0, "evicted": 0}
        self._maintenance_thread: Optional[threading.Thread] = None
        self._running = False

    def acquire(self, timeout: float = 30.0) -> Resource[T]:
        try:
            resource = self._idle.get_nowait()
            if resource.is_valid():
                resource.acquire()
                self._stats["acquired"] += 1
                return resource
            else:
                self._destroy_resource(resource)
        except Empty:
            pass
        with self._lock:
            if len(self._all) < self._max_size:
                resource = self._factory()
                self._all.append(resource)
                self._stats["created"] += 1
                resource.acquire()
                self._stats["acquired"] += 1
                return resource
        try:
            resource = self._idle.get(timeout=timeout)
            resource.acquire()
            self._stats["acquired"] += 1
            return resource
        except Empty:
            raise RuntimeError("Resource pool exhausted")

    def release(self, resource: Resource[T]) -> None:
        resource.release()
        if resource.is_valid():
            self._idle.put(resource)
            self._stats["released"] += 1
        else:
            self._destroy_resource(resource)

    def _destroy_resource(self, resource: Resource[T]) -> None:
        resource.close()
        with self._lock:
            if resource in self._all:
                self._all.remove(resource)
        self._stats["destroyed"] += 1

    def start_maintenance(self, interval: float = 60.0) -> None:
        self._running = True
        self._maintenance_thread = threading.Thread(
            target=self._maintenance_loop, args=(interval,), daemon=True
        )
        self._maintenance_thread.start()

    def stop_maintenance(self) -> None:
        self._running = False
        if self._maintenance_thread:
            self._maintenance_thread.join(timeout=5)

    def _maintenance_loop(self, interval: float) -> None:
        while self._running:
            self._evict_idle()
            self._ensure_min_idle()
            time.sleep(interval)

    def _evict_idle(self) -> None:
        temp: List[Resource[T]] = []
        while not self._idle.empty():
            try:
                resource = self._idle.get_nowait()
                if resource.idle_time > self._max_idle_time or \
                   resource.age > self._max_lifetime or \
                   not resource.is_valid():
                    self._destroy_resource(resource)
                    self._stats["evicted"] += 1
                else:
                    temp.append(resource)
            except Empty:
                break
        for r in temp:
            self._idle.put(r)

    def _ensure_min_idle(self) -> None:
        with self._lock:
            idle_count = self._idle.qsize()
            total = len(self._all)
            needed = self._min_idle - idle_count
            can_create = self._max_size - total
            to_create = min(needed, can_create)
        for _ in range(max(0, to_create)):
            try:
                resource = self._factory()
                with self._lock:
                    self._all.append(resource)
                self._idle.put(resource)
                self._stats["created"] += 1
            except Exception:
                break

    @property
    def stats(self) -> Dict[str, int]:
        with self._lock:
            return dict(self._stats)

    @property
    def idle_count(self) -> int:
        return self._idle.qsize()

    @property
    def total_count(self) -> int:
        with self._lock:
            return len(self._all)

    @property
    def in_use_count(self) -> int:
        with self._lock:
            return sum(1 for r in self._all if r.in_use)

    def close_all(self) -> None:
        self.stop_maintenance()
        while not self._idle.empty():
            try:
                resource = self._idle.get_nowait()
                self._destroy_resource(resource)
            except Empty:
                break
        with self._lock:
            for resource in list(self._all):
                if not resource.in_use:
                    self._destroy_resource(resource)

class PoolContext:
    def __init__(self, pool: ResourcePool, timeout: float = 30.0):
        self._pool = pool
        self._timeout = timeout
        self._resource: Optional[Resource] = None

    def __enter__(self) -> Resource:
        self._resource = self._pool.acquire(self._timeout)
        return self._resource

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._resource:
            self._pool.release(self._resource)
            self._resource = None
        return False
