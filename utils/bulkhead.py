#!/usr/bin/env python3
"""Bulkhead pattern for resource isolation and fault tolerance."""
from typing import Dict, Optional, List, Any, Callable
from dataclasses import dataclass, field
from collections import defaultdict
import time
import threading
from concurrent.futures import ThreadPoolExecutor, Future

@dataclass
class BulkheadConfig:
    name: str
    max_concurrent: int = 10
    max_queue: int = 20
    timeout: float = 30.0

class Bulkhead:
    def __init__(self, config: BulkheadConfig):
        self._config = config
        self._executor = ThreadPoolExecutor(
            max_workers=config.max_concurrent,
            thread_name_prefix=f"bulkhead-{config.name}"
        )
        self._active = 0
        self._queued = 0
        self._lock = threading.Lock()
        self._rejected = 0
        self._completed = 0
        self._failed = 0
        self._callbacks: List[Callable] = []

    def submit(self, fn: Callable, *args, **kwargs) -> Optional[Future]:
        with self._lock:
            if self._active + self._queued >= self._config.max_queue:
                self._rejected += 1
                self._fire("reject", self._config.name)
                return None
            self._queued += 1

        def _wrapper():
            with self._lock:
                self._queued -= 1
                self._active += 1
            try:
                result = fn(*args, **kwargs)
                with self._lock:
                    self._completed += 1
                self._fire("complete", self._config.name)
                return result
            except Exception as e:
                with self._lock:
                    self._failed += 1
                self._fire("error", self._config.name, e)
                raise
            finally:
                with self._lock:
                    self._active -= 1

        return self._executor.submit(_wrapper)

    def execute(self, fn: Callable, *args, **kwargs) -> Any:
        future = self.submit(fn, *args, **kwargs)
        if future is None:
            raise RuntimeError(f"Bulkhead {self._config.name} is full")
        return future.result(timeout=self._config.timeout)

    @property
    def stats(self) -> Dict[str, int]:
        with self._lock:
            return {
                "active": self._active,
                "queued": self._queued,
                "completed": self._completed,
                "failed": self._failed,
                "rejected": self._rejected,
                "available": max(0, self._config.max_concurrent - self._active),
            }

    def on_event(self, callback: Callable) -> None:
        self._callbacks.append(callback)

    def _fire(self, event: str, name: str, *args) -> None:
        for cb in self._callbacks:
            try:
                cb(event, name, *args)
            except Exception:
                pass

    def shutdown(self, wait: bool = True) -> None:
        self._executor.shutdown(wait=wait)

class BulkheadRegistry:
    def __init__(self):
        self._bulkheads: Dict[str, Bulkhead] = {}
        self._lock = threading.Lock()

    def register(self, config: BulkheadConfig) -> Bulkhead:
        with self._lock:
            bulkhead = Bulkhead(config)
            self._bulkheads[config.name] = bulkhead
            return bulkhead

    def get(self, name: str) -> Optional[Bulkhead]:
        with self._lock:
            return self._bulkheads.get(name)

    def shutdown_all(self) -> None:
        with self._lock:
            for bulkhead in self._bulkheads.values():
                bulkhead.shutdown(wait=False)
            self._bulkheads.clear()

    def all_stats(self) -> Dict[str, Dict[str, int]]:
        with self._lock:
            return {name: b.stats for name, b in self._bulkheads.items()}
