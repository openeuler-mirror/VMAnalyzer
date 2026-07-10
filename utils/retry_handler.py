#!/usr/bin/env python3
"""Retry handler with exponential backoff and jitter."""
from typing import Callable, Any, Optional, List, Type
import time
import random

class RetryConfig:
    def __init__(self, max_attempts: int = 3, base_delay: float = 1.0,
                 max_delay: float = 60.0, exponential_base: float = 2.0,
                 jitter: bool = True):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter

    def get_delay(self, attempt: int) -> float:
        delay = self.base_delay * (self.exponential_base ** (attempt - 1))
        delay = min(delay, self.max_delay)
        if self.jitter:
            delay = delay * (0.5 + random.random() * 0.5)
        return delay

class RetryHandler:
    def __init__(self, config: Optional[RetryConfig] = None,
                 retry_exceptions: Optional[List[Type[Exception]]] = None):
        self._config = config or RetryConfig()
        self._retry_exceptions = retry_exceptions or [Exception]
        self._attempts: List[dict] = []

    def execute(self, func: Callable, *args, **kwargs) -> Any:
        last_exception = None
        for attempt in range(1, self._config.max_attempts + 1):
            try:
                result = func(*args, **kwargs)
                self._attempts.append({"attempt": attempt, "success": True})
                return result
            except Exception as e:
                last_exception = e
                self._attempts.append({"attempt": attempt, "success": False, "error": str(e)})
                should_retry = any(isinstance(e, exc) for exc in self._retry_exceptions)
                if not should_retry or attempt >= self._config.max_attempts:
                    raise
                delay = self._config.get_delay(attempt)
                time.sleep(delay)
        raise last_exception

    def execute_async(self, func: Callable, *args, **kwargs) -> Any:
        return self.execute(func, *args, **kwargs)

    @property
    def history(self) -> List[dict]:
        return list(self._attempts)

    @property
    def total_attempts(self) -> int:
        return len(self._attempts)

    def reset(self) -> None:
        self._attempts.clear()

class CircuitRetryHandler:
    def __init__(self, retry_config: Optional[RetryConfig] = None,
                 failure_threshold: int = 10):
        self._retry = RetryHandler(retry_config)
        self._failure_threshold = failure_threshold
        self._consecutive_failures = 0
        self._circuit_open = False

    def execute(self, func: Callable, *args, **kwargs) -> Any:
        if self._circuit_open:
            raise RuntimeError("Circuit is open due to repeated failures")
        try:
            result = self._retry.execute(func, *args, **kwargs)
            self._consecutive_failures = 0
            return result
        except Exception:
            self._consecutive_failures += 1
            if self._consecutive_failures >= self._failure_threshold:
                self._circuit_open = True
            raise

    def reset_circuit(self) -> None:
        self._circuit_open = False
        self._consecutive_failures = 0
