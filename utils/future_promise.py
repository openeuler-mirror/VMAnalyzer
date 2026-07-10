#!/usr/bin/env python3
"""Future and promise pattern for asynchronous result handling."""
from typing import Any, Callable, Optional, List, TypeVar, Generic
import threading
import time
from enum import Enum

T = TypeVar("T")

class FutureState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Promise(Generic[T]):
    def __init__(self):
        self._state = FutureState.PENDING
        self._result: Optional[T] = None
        self._error: Optional[Exception] = None
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._callbacks: List[Callable] = []
        self._error_callbacks: List[Callable] = []
        self._finally_callbacks: List[Callable] = []

    def set_result(self, result: T) -> None:
        with self._condition:
            if self._state != FutureState.PENDING and self._state != FutureState.RUNNING:
                raise RuntimeError(f"Cannot set result on {self._state} promise")
            self._result = result
            self._state = FutureState.COMPLETED
            callbacks = list(self._callbacks)
            finally_cbs = list(self._finally_callbacks)
            self._condition.notify_all()
        for cb in callbacks:
            try:
                cb(result)
            except Exception:
                pass
        for cb in finally_cbs:
            try:
                cb()
            except Exception:
                pass

    def set_error(self, error: Exception) -> None:
        with self._condition:
            if self._state != FutureState.PENDING and self._state != FutureState.RUNNING:
                raise RuntimeError(f"Cannot set error on {self._state} promise")
            self._error = error
            self._state = FutureState.FAILED
            callbacks = list(self._error_callbacks)
            finally_cbs = list(self._finally_callbacks)
            self._condition.notify_all()
        for cb in callbacks:
            try:
                cb(error)
            except Exception:
                pass
        for cb in finally_cbs:
            try:
                cb()
            except Exception:
                pass

    def set_running(self) -> None:
        with self._lock:
            if self._state != FutureState.PENDING:
                raise RuntimeError(f"Cannot set running on {self._state} promise")
            self._state = FutureState.RUNNING

    def cancel(self) -> bool:
        with self._condition:
            if self._state in (FutureState.COMPLETED, FutureState.FAILED, FutureState.CANCELLED):
                return False
            self._state = FutureState.CANCELLED
            finally_cbs = list(self._finally_callbacks)
            self._condition.notify_all()
        for cb in finally_cbs:
            try:
                cb()
            except Exception:
                pass
        return True

class Future(Generic[T]):
    def __init__(self, promise: Promise[T]):
        self._promise = promise

    @property
    def state(self) -> FutureState:
        with self._promise._lock:
            return self._promise._state

    @property
    def is_done(self) -> bool:
        return self.state in (FutureState.COMPLETED, FutureState.FAILED, FutureState.CANCELLED)

    def get(self, timeout: Optional[float] = None) -> T:
        with self._promise._condition:
            while not self.is_done:
                if not self._promise._condition.wait(timeout):
                    raise TimeoutError("Future timed out")
            if self._promise._state == FutureState.COMPLETED:
                return self._promise._result
            elif self._promise._state == FutureState.FAILED:
                raise self._promise._error
            elif self._promise._state == FutureState.CANCELLED:
                raise RuntimeError("Future was cancelled")
        return None

    def then(self, callback: Callable[[T], Any]) -> "Future":
        def wrapper(result):
            try:
                callback(result)
            except Exception:
                pass
        with self._promise._lock:
            if self._promise._state == FutureState.COMPLETED:
                wrapper(self._promise._result)
            else:
                self._promise._callbacks.append(wrapper)
        return self

    def catch(self, callback: Callable[[Exception], Any]) -> "Future":
        with self._promise._lock:
            if self._promise._state == FutureState.FAILED:
                callback(self._promise._error)
            else:
                self._promise._error_callbacks.append(callback)
        return self

    def finally_(self, callback: Callable[[], Any]) -> "Future":
        with self._promise._lock:
            if self.is_done:
                callback()
            else:
                self._promise._finally_callbacks.append(callback)
        return self

    def cancel(self) -> bool:
        return self._promise.cancel()

class FutureUtils:
    @staticmethod
    def all_futures(futures: List[Future]) -> Future:
        promise = Promise()
        results = [None] * len(futures)
        remaining = [len(futures)]
        lock = threading.Lock()

        def make_callback(index):
            def callback(result):
                with lock:
                    results[index] = result
                    remaining[0] -= 1
                    if remaining[0] == 0:
                        promise.set_result(results)
            return callback

        def error_callback(error):
            promise.set_error(error)

        for i, future in enumerate(futures):
            future.then(make_callback(i)).catch(error_callback)
        return Future(promise)

    @staticmethod
    def any_future(futures: List[Future]) -> Future:
        promise = Promise()
        for future in futures:
            future.then(lambda r: promise.set_result(r) if not promise.is_done else None)
            future.catch(lambda e: None)
        return Future(promise)

    @staticmethod
    def resolved(value: T) -> Future:
        promise = Promise()
        promise.set_result(value)
        return Future(promise)

    @staticmethod
    def rejected(error: Exception) -> Future:
        promise = Promise()
        promise.set_error(error)
        return Future(promise)

    @staticmethod
    def delay(seconds: float, value: T = None) -> Future:
        promise = Promise()
        def timer():
            time.sleep(seconds)
            promise.set_result(value)
        threading.Thread(target=timer, daemon=True).start()
        return Future(promise)
