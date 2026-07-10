#!/usr/bin/env python3
"""Task scheduler with periodic and one-time job execution."""
from typing import Callable, Any, Optional, List, Dict
import threading
import time
from enum import Enum

class JobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Job:
    def __init__(self, func: Callable, name: str = "", interval: float = 0,
                 max_runs: int = -1, args: tuple = (), kwargs: dict = None):
        self._func = func
        self._name = name or func.__name__
        self._interval = interval
        self._max_runs = max_runs
        self._args = args
        self._kwargs = kwargs or {}
        self._status = JobStatus.PENDING
        self._run_count = 0
        self._last_run: Optional[float] = None
        self._next_run: Optional[float] = None
        self._lock = threading.Lock()
        self._results: List[Any] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def status(self) -> JobStatus:
        return self._status

    @property
    def interval(self) -> float:
        return self._interval

    @property
    def run_count(self) -> int:
        return self._run_count

    def should_run(self) -> bool:
        if self._status == JobStatus.CANCELLED:
            return False
        if self._max_runs > 0 and self._run_count >= self._max_runs:
            return False
        if self._next_run is None:
            return True
        return time.time() >= self._next_run

    def execute(self) -> Any:
        with self._lock:
            if self._status == JobStatus.CANCELLED:
                return None
            self._status = JobStatus.RUNNING
        try:
            result = self._func(*self._args, **self._kwargs)
            self._results.append(result)
            self._status = JobStatus.COMPLETED
            self._run_count += 1
            self._last_run = time.time()
            if self._interval > 0:
                self._next_run = time.time() + self._interval
            return result
        except Exception as e:
            self._status = JobStatus.FAILED
            self._run_count += 1
            self._last_run = time.time()
            if self._interval > 0:
                self._next_run = time.time() + self._interval
            raise

    def cancel(self) -> None:
        self._status = JobStatus.CANCELLED

    @property
    def results(self) -> List[Any]:
        return list(self._results)

class TaskScheduler:
    def __init__(self):
        self._jobs: Dict[str, Job] = {}
        self._lock = threading.Lock()
        self._running = False
        self._thread: Optional[threading.Thread] = None

    def add_job(self, job: Job) -> str:
        with self._lock:
            self._jobs[job.name] = job
        return job.name

    def remove_job(self, name: str) -> bool:
        with self._lock:
            if name in self._jobs:
                self._jobs[name].cancel()
                del self._jobs[name]
                return True
            return False

    def start(self) -> None:
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)

    def _run_loop(self) -> None:
        while self._running:
            for job in list(self._jobs.values()):
                if job.should_run():
                    try:
                        job.execute()
                    except Exception:
                        pass
            time.sleep(0.1)

    def get_job(self, name: str) -> Optional[Job]:
        return self._jobs.get(name)

    def list_jobs(self) -> List[str]:
        return list(self._jobs.keys())

    def job_count(self) -> int:
        return len(self._jobs)
