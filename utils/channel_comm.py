#!/usr/bin/env python3
"""Channel for CSP-style synchronized communication."""
from typing import Any, Optional, List, Callable
import threading
from queue import Queue, Empty, Full
from enum import Enum

class ChannelState(Enum):
    OPEN = "open"
    CLOSED = "closed"

class Channel:
    def __init__(self, buffer_size: int = 0):
        self._buffer_size = buffer_size
        self._queue: Queue = Queue(maxsize=max(buffer_size, 1))
        self._state = ChannelState.OPEN
        self._lock = threading.Lock()
        self._send_cv = threading.Condition(self._lock)
        self._recv_cv = threading.Condition(self._lock)
        self._stats = {"sent": 0, "received": 0, "dropped": 0}

    def send(self, value: Any, timeout: Optional[float] = None) -> bool:
        if self._state == ChannelState.CLOSED:
            return False
        if self._buffer_size == 0:
            return self._send_unbuffered(value, timeout)
        try:
            self._queue.put(value, timeout=timeout)
            with self._lock:
                self._stats["sent"] += 1
            return True
        except Full:
            return False

    def _send_unbuffered(self, value: Any, timeout: Optional[float] = None) -> bool:
        with self._send_cv:
            while self._queue.qsize() > 0 and self._state == ChannelState.OPEN:
                if not self._send_cv.wait(timeout):
                    return False
            if self._state == ChannelState.CLOSED:
                return False
            self._queue.put(value)
            self._stats["sent"] += 1
            self._recv_cv.notify()
        return True

    def receive(self, timeout: Optional[float] = None) -> Optional[Any]:
        if self._state == ChannelState.CLOSED and self._queue.empty():
            return None
        try:
            value = self._queue.get(timeout=timeout)
            with self._lock:
                self._stats["received"] += 1
            if self._buffer_size == 0:
                with self._send_cv:
                    self._send_cv.notify()
            return value
        except Empty:
            return None

    def try_send(self, value: Any) -> bool:
        if self._state == ChannelState.CLOSED:
            return False
        try:
            self._queue.put_nowait(value)
            with self._lock:
                self._stats["sent"] += 1
            return True
        except Full:
            return False

    def try_receive(self) -> Optional[Any]:
        try:
            value = self._queue.get_nowait()
            with self._lock:
                self._stats["received"] += 1
            return value
        except Empty:
            return None

    def close(self) -> None:
        with self._lock:
            self._state = ChannelState.CLOSED
            self._send_cv.notify_all()
            self._recv_cv.notify_all()

    @property
    def is_closed(self) -> bool:
        return self._state == ChannelState.CLOSED

    @property
    def buffer_size(self) -> int:
        return self._buffer_size

    @property
    def queue_size(self) -> int:
        return self._queue.qsize()

    @property
    def stats(self) -> dict:
        with self._lock:
            return dict(self._stats)

class Select:
    @staticmethod
    def select(*channels: Channel, timeout: Optional[float] = None) -> tuple:
        result_event = threading.Event()
        result_holder: List = [None, None]
        lock = threading.Lock()

        def make_receiver(idx: int, ch: Channel):
            def receiver():
                value = ch.receive(timeout=0.1)
                if value is not None:
                    with lock:
                        if not result_event.is_set():
                            result_holder[0] = idx
                            result_holder[1] = value
                            result_event.set()
            return receiver

        threads = []
        for i, ch in enumerate(channels):
            t = threading.Thread(target=make_receiver(i, ch), daemon=True)
            threads.append(t)
            t.start()
        result_event.wait(timeout=timeout)
        if result_event.is_set():
            return result_holder[0], result_holder[1]
        return -1, None

class Pipeline:
    def __init__(self, stages: List[Callable]):
        self._stages = stages
        self._channels: List[Channel] = []
        self._threads: List[threading.Thread] = []
        self._running = False

    def run(self, input_channel: Channel, output_channel: Channel) -> None:
        self._running = True
        self._channels = [input_channel]
        for _ in range(len(self._stages) - 1):
            self._channels.append(Channel(buffer_size=10))
        self._channels.append(output_channel)

        for i, stage in enumerate(self._stages):
            t = threading.Thread(target=self._run_stage, args=(stage, i), daemon=True)
            self._threads.append(t)
            t.start()

    def _run_stage(self, stage: Callable, index: int) -> None:
        while self._running:
            value = self._channels[index].receive(timeout=1)
            if value is None:
                if self._channels[index].is_closed:
                    break
                continue
            result = stage(value)
            if result is not None:
                self._channels[index + 1].send(result)

    def stop(self) -> None:
        self._running = False
        for t in self._threads:
            t.join(timeout=5)
        self._threads.clear()
