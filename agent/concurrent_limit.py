#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Limit concurrent VM collections."""
import threading, time, logging
LOG=logging.getLogger(__name__)

class ConcurrentCollectionLimiter:
    """Semaphore-based concurrency control for VM collections."""
    def __init__(self,max_concurrent=10):
        self.semaphore=threading.BoundedSemaphore(max_concurrent)
        self.active_count=0; self._lock=threading.Lock()

    def acquire(self,timeout=5):
        acquired=self.semaphore.acquire(timeout=timeout)
        if acquired:
            with self._lock: self.active_count+=1
        return acquired

    def release(self):
        self.semaphore.release()
        with self._lock: self.active_count-=1

    def get_active_count(self):
        with self._lock: return self.active_count

    def __enter__(self):
        self.acquire(); return self

    def __exit__(self,*args):
        self.release()
