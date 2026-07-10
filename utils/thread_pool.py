#!/usr/bin/env python3
"""Thread pool for concurrent task execution with futures."""
from typing import Callable, Any, List, Optional, Dict
import threading
import queue
from concurrent.futures import Future
import time

class ThreadPool:
    def __init__(self, num_workers: int = 4, max_queue_size: int = 1000):
        self._num_workers = num_workers
        self._task_queue: queue.Queue = queue.Queue(maxsize=max_queue_size)
        self._workers: List[threading.Thread] = []
        self._running = False
        self._lock = threading.Lock()
        self._stats = {"submitted": 0, "completed": 0, "failed": 0}
        self._active_count = 0

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        for i in range(self._num_workers):
            t = threading.Thread(target=self._worker_loop, daemon=True, name=f"pool-worker-{i}")
            self._workers.append(t)
            t.start()

    def stop(self, wait: bool = True) -> None:
        self._running = False
        for _ in range(self._num_workers):
            self._task_queue.put(None)
        if wait:
            for t in self._workers:
                t.join(timeout=5)
        self._workers.clear()

    def submit(self, func: Callable, *args, **kwargs) -> Future:
        future = Future()
        task = (func, args, kwargs, future)
        self._task_queue.put(task)
        with self._lock:
            self._stats["submitted"] += 1
        return future

    def map(self, func: Callable, iterable: List) -> List[Future]:
        return [self.submit(func, item) for item in iterable]

    def _worker_loop(self) -> None:
        while self._running:
            try:
                task = self._task_queue.get(timeout=1)
                if task is None:
                    break
                func, args, kwargs, future = task
                with self._lock:
                    self._active_count += 1
                try:
                    result = func(*args, **kwargs)
                    future.set_result(result)
                    with self._lock:
                        self._stats["completed"] += 1
                except Exception as e:
                    future.set_exception(e)
                    with self._lock:
                        self._stats["failed"] += 1
                finally:
                    with self._lock:
                        self._active_count -= 1
                    self._task_queue.task_done()
            except queue.Empty:
                continue

    def wait_all(self, timeout: Optional[float] = None) -> None:
        self._task_queue.join()

    @property
    def stats(self) -> Dict[str, int]:
        with self._lock:
            return dict(self._stats)

    @property
    def queue_size(self) -> int:
        return self._task_queue.qsize()

    @property
    def active_workers(self) -> int:
        return self._active_count

    @property
    def worker_count(self) -> int:
        return self._num_workers

    def resize(self, new_size: int) -> None:
        old_running = self._running
        self.stop(wait=False)
        self._num_workers = new_size
        self._task_queue = queue.Queue(maxsize=1000)
        if old_running:
            self.start()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop(wait=True)
        return False
