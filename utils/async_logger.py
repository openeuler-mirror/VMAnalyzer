#!/usr/bin/env python3
"""Async logger with buffered file writing and log rotation."""
from typing import Optional, List, Dict, Any
import threading
import time
import os
from queue import Queue, Full
from enum import Enum

class LogLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

class LogRecord:
    def __init__(self, level: LogLevel, message: str, logger_name: str = "",
                 extra: Optional[Dict] = None):
        self._level = level
        self._message = message
        self._logger = logger_name
        self._timestamp = time.time()
        self._extra = extra or {}
        self._thread_id = threading.get_ident()

    @property
    def level(self) -> LogLevel:
        return self._level

    @property
    def message(self) -> str:
        return self._message

    @property
    def timestamp(self) -> float:
        return self._timestamp

    def format(self) -> str:
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self._timestamp))
        return f"[{ts}] [{self._level.name}] [{self._thread_id}] {self._message}"

class AsyncLogger:
    def __init__(self, name: str = "app", filepath: Optional[str] = None,
                 level: LogLevel = LogLevel.INFO, buffer_size: int = 1000,
                 max_file_size: int = 10 * 1024 * 1024, backup_count: int = 5):
        self._name = name
        self._filepath = filepath
        self._level = level
        self._buffer: Queue = Queue(maxsize=buffer_size)
        self._max_file_size = max_file_size
        self._backup_count = backup_count
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        self._stats = {"logged": 0, "dropped": 0, "flushed": 0}
        self._handlers: List = []

    def add_handler(self, handler) -> None:
        self._handlers.append(handler)

    def log(self, level: LogLevel, message: str, extra: Optional[Dict] = None) -> None:
        if level.value < self._level.value:
            return
        record = LogRecord(level, message, self._name, extra)
        try:
            self._buffer.put_nowait(record)
            with self._lock:
                self._stats["logged"] += 1
        except Full:
            with self._lock:
                self._stats["dropped"] += 1

    def debug(self, msg: str) -> None: self.log(LogLevel.DEBUG, msg)
    def info(self, msg: str) -> None: self.log(LogLevel.INFO, msg)
    def warning(self, msg: str) -> None: self.log(LogLevel.WARNING, msg)
    def error(self, msg: str) -> None: self.log(LogLevel.ERROR, msg)
    def critical(self, msg: str) -> None: self.log(LogLevel.CRITICAL, msg)

    def start(self) -> None:
        self._running = True
        self._thread = threading.Thread(target=self._flush_loop, daemon=True)
        self._thread.start()

    def stop(self, flush: bool = True) -> None:
        self._running = False
        if flush:
            self._flush_all()
        if self._thread:
            self._thread.join(timeout=5)

    def _flush_loop(self) -> None:
        while self._running:
            self._flush_batch()
            time.sleep(0.1)

    def _flush_batch(self, batch_size: int = 100) -> None:
        records = []
        for _ in range(min(batch_size, self._buffer.qsize())):
            try:
                records.append(self._buffer.get_nowait())
            except Exception:
                break
        if not records:
            return
        for handler in self._handlers:
            for record in records:
                try:
                    handler(record)
                except Exception:
                    pass
        if self._filepath:
            self._write_to_file(records)
        with self._lock:
            self._stats["flushed"] += len(records)

    def _flush_all(self) -> None:
        while not self._buffer.empty():
            self._flush_batch(batch_size=1000)

    def _write_to_file(self, records: List[LogRecord]) -> None:
        if self._filepath and os.path.exists(self._filepath):
            if os.path.getsize(self._filepath) >= self._max_file_size:
                self._rotate()
        with open(self._filepath, "a") as f:
            for record in records:
                f.write(record.format() + "\n")

    def _rotate(self) -> None:
        for i in range(self._backup_count - 1, 0, -1):
            src = f"{self._filepath}.{i}"
            dst = f"{self._filepath}.{i + 1}"
            if os.path.exists(src):
                os.rename(src, dst)
        if os.path.exists(self._filepath):
            os.rename(self._filepath, f"{self._filepath}.1")

    @property
    def stats(self) -> Dict[str, int]:
        with self._lock:
            return dict(self._stats)

    @property
    def buffer_size(self) -> int:
        return self._buffer.qsize()

    def set_level(self, level: LogLevel) -> None:
        self._level = level
