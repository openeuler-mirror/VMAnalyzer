#!/usr/bin/env python3
"""Backpressure handler for managing flow control."""
from typing import Callable, Any, Optional, List, Dict
from enum import Enum
import threading
import time
from collections import deque

class BackpressureStrategy(Enum):
    BLOCK = "block"
    DROP = "drop"
    BUFFER = "buffer"
    SAMPLE = "sample"

class BackpressureHandler:
    def __init__(self, strategy: BackpressureStrategy = BackpressureStrategy.BLOCK,
                 max_buffer_size: int = 1000, high_watermark: float = 0.8,
                 low_watermark: float = 0.2, sample_rate: float = 0.5):
        self._strategy = strategy
        self._max_buffer = max_buffer_size
        self._high = high_watermark
        self._low = low_watermark
        self._sample_rate = sample_rate
        self._buffer: deque = deque()
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._stats = {"accepted": 0, "dropped": 0, "blocked": 0, "sampled": 0}
        self._consumer: Optional[Callable] = None
        self._running = False
        self._thread: Optional[threading.Thread] = None

    def set_consumer(self, consumer: Callable) -> None:
        self._consumer = consumer

    def submit(self, item: Any) -> bool:
        with self._lock:
            buffer_ratio = len(self._buffer) / self._max_buffer
            if buffer_ratio >= self._high:
                if self._strategy == BackpressureStrategy.DROP:
                    self._stats["dropped"] += 1
                    return False
                elif self._strategy == BackpressureStrategy.SAMPLE:
                    if len(self._buffer) > 0:
                        self._buffer.popleft()
                        self._stats["sampled"] += 1
                elif self._strategy == BackpressureStrategy.BLOCK:
                    while len(self._buffer) >= self._max_buffer:
                        self._stats["blocked"] += 1
                        self._condition.wait(timeout=1)
                        if not self._running:
                            return False
            self._buffer.append(item)
            self._stats["accepted"] += 1
            self._condition.notify()
            return True

    def start(self) -> None:
        self._running = True
        self._thread = threading.Thread(target=self._consume_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False
        with self._condition:
            self._condition.notify_all()
        if self._thread:
            self._thread.join(timeout=5)

    def _consume_loop(self) -> None:
        while self._running:
            with self._condition:
                while not self._buffer and self._running:
                    self._condition.wait(timeout=1)
                if not self._running:
                    break
                item = self._buffer.popleft()
                buffer_ratio = len(self._buffer) / self._max_buffer
                if buffer_ratio < self._low:
                    self._condition.notify_all()
            if self._consumer and item is not None:
                try:
                    self._consumer(item)
                except Exception:
                    pass

    @property
    def stats(self) -> Dict[str, int]:
        with self._lock:
            return dict(self._stats)

    @property
    def buffer_size(self) -> int:
        with self._lock:
            return len(self._buffer)

    @property
    def buffer_ratio(self) -> float:
        with self._lock:
            return len(self._buffer) / self._max_buffer

    def is_overloaded(self) -> bool:
        return self.buffer_ratio >= self._high

    def flush(self) -> int:
        count = 0
        with self._lock:
            while self._buffer:
                item = self._buffer.popleft()
                count += 1
                if self._consumer:
                    try:
                        self._consumer(item)
                    except Exception:
                        pass
            self._condition.notify_all()
        return count

    def set_strategy(self, strategy: BackpressureStrategy) -> None:
        self._strategy = strategy

    def resize_buffer(self, new_size: int) -> None:
        with self._lock:
            self._max_buffer = new_size
            while len(self._buffer) > new_size:
                self._buffer.popleft()
            self._condition.notify_all()
