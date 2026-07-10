#!/usr/bin/env python3
"""Message queue with priority and delayed delivery."""
from typing import Any, Optional, Dict, List, Callable
import threading
import time
from queue import PriorityQueue
from enum import Enum

class MessagePriority(Enum):
    LOW = 3
    NORMAL = 2
    HIGH = 1
    URGENT = 0

class Message:
    _counter = 0
    _counter_lock = threading.Lock()

    def __init__(self, body: Any, priority: MessagePriority = MessagePriority.NORMAL,
                 delay: float = 0, headers: Optional[Dict] = None):
        with Message._counter_lock:
            Message._counter += 1
            self._id = Message._counter
        self._body = body
        self._priority = priority
        self._delay = delay
        self._headers = headers or {}
        self._created = time.time()
        self._deliver_at = time.time() + delay
        self._retry_count = 0
        self._max_retries = 3

    @property
    def id(self) -> int:
        return self._id

    @property
    def body(self) -> Any:
        return self._body

    @property
    def priority(self) -> MessagePriority:
        return self._priority

    @property
    def deliver_at(self) -> float:
        return self._deliver_at

    @property
    def headers(self) -> Dict:
        return dict(self._headers)

    def add_header(self, key: str, value: Any) -> None:
        self._headers[key] = value

    def can_deliver(self) -> bool:
        return time.time() >= self._deliver_at

    def increment_retry(self) -> bool:
        self._retry_count += 1
        self._deliver_at = time.time() + (self._retry_count ** 2)
        return self._retry_count <= self._max_retries

    @property
    def retry_count(self) -> int:
        return self._retry_count

class MessageQueue:
    def __init__(self, max_size: int = 10000):
        self._queue: PriorityQueue = PriorityQueue(maxsize=max_size)
        self._consumers: List[Callable] = []
        self._running = False
        self._threads: List[threading.Thread] = []
        self._stats = {"enqueued": 0, "delivered": 0, "failed": 0, "retried": 0}
        self._lock = threading.Lock()
        self._dead_letter: List[Message] = []

    def enqueue(self, message: Message) -> bool:
        try:
            self._queue.put((message._priority.value, message._id, message), timeout=1)
            with self._lock:
                self._stats["enqueued"] += 1
            return True
        except Exception:
            return False

    def dequeue(self, timeout: float = 1.0) -> Optional[Message]:
        try:
            _, _, msg = self._queue.get(timeout=timeout)
            if msg.can_deliver():
                return msg
            else:
                self._queue.put((msg._priority.value, msg._id, msg))
                return None
        except Exception:
            return None

    def add_consumer(self, consumer: Callable) -> None:
        self._consumers.append(consumer)

    def start(self, num_workers: int = 1) -> None:
        self._running = True
        for i in range(num_workers):
            t = threading.Thread(target=self._consume_loop, daemon=True, name=f"mq-worker-{i}")
            self._threads.append(t)
            t.start()

    def stop(self) -> None:
        self._running = False
        for t in self._threads:
            t.join(timeout=5)
        self._threads.clear()

    def _consume_loop(self) -> None:
        while self._running:
            msg = self.dequeue(timeout=1)
            if msg is None:
                continue
            delivered = False
            for consumer in list(self._consumers):
                try:
                    consumer(msg)
                    delivered = True
                    with self._lock:
                        self._stats["delivered"] += 1
                    break
                except Exception:
                    continue
            if not delivered:
                if msg.increment_retry():
                    self.enqueue(msg)
                    with self._lock:
                        self._stats["retried"] += 1
                else:
                    self._dead_letter.append(msg)
                    with self._lock:
                        self._stats["failed"] += 1

    @property
    def stats(self) -> Dict[str, int]:
        with self._lock:
            return dict(self._stats)

    @property
    def queue_size(self) -> int:
        return self._queue.qsize()

    @property
    def dead_letter_count(self) -> int:
        return len(self._dead_letter)

    def get_dead_letters(self) -> List[Message]:
        return list(self._dead_letter)

    def clear_dead_letters(self) -> int:
        count = len(self._dead_letter)
        self._dead_letter.clear()
        return count

    def purge(self) -> int:
        count = 0
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
                count += 1
            except Exception:
                break
        return count
