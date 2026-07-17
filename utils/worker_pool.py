#!/usr/bin/env python3
"""Simple worker thread pool for parallel task execution."""
import threading
import queue
from typing import Callable, List

class WorkerPool:
    """A simple thread pool for executing tasks concurrently."""

    def __init__(self, num_workers: int = 4):
        self._queue: queue.Queue = queue.Queue()
        self._workers: List[threading.Thread] = []
        self._running = True
        for _ in range(num_workers):
            t = threading.Thread(target=self._worker_loop, daemon=True)
            t.start()
            self._workers.append(t)

    def submit(self, task: Callable, *args) -> None:
        """Submit a task to the pool."""
        self._queue.put((task, args))

    def _worker_loop(self) -> None:
        while self._running:
            try:
                task, args = self._queue.get(timeout=1)
                task(*args)
                self._queue.task_done()
            except queue.Empty:
                continue
            except Exception:
                pass

    def wait(self) -> None:
        """Wait for all submitted tasks to complete."""
        self._queue.join()

    def shutdown(self) -> None:
        """Shutdown the worker pool."""
        self._running = False
        for w in self._workers:
            w.join(timeout=2)

    def pending(self) -> int:
        """Return number of pending tasks."""
        return self._queue.qsize()
