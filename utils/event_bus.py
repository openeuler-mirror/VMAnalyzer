#!/usr/bin/env python3
"""Event bus for publish/subscribe communication."""
from typing import Callable, Dict, List, Any
import weakref

class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._history: List[Dict] = []
        self._max_history = 100

    def subscribe(self, event: str, handler: Callable) -> "EventBus":
        if event not in self._subscribers:
            self._subscribers[event] = []
        self._subscribers[event].append(handler)
        return self

    def unsubscribe(self, event: str, handler: Callable) -> bool:
        if event in self._subscribers:
            try:
                self._subscribers[event].remove(handler)
                return True
            except ValueError:
                pass
        return False

    def publish(self, event: str, data: Any = None) -> int:
        count = 0
        if event in self._subscribers:
            for handler in list(self._subscribers[event]):
                try:
                    handler(data)
                    count += 1
                except Exception as e:
                    self._log_error(event, str(e))
        self._history.append({"event": event, "data": data, "delivered": count})
        if len(self._history) > self._max_history:
            self._history.pop(0)
        return count

    def publish_async(self, event: str, data: Any = None) -> None:
        import threading
        threading.Thread(target=self.publish, args=(event, data), daemon=True).start()

    def subscriber_count(self, event: str) -> int:
        return len(self._subscribers.get(event, []))

    def events(self) -> List[str]:
        return list(self._subscribers.keys())

    def clear(self) -> None:
        self._subscribers.clear()
        self._history.clear()

    def history(self) -> List[Dict]:
        return list(self._history)

    def _log_error(self, event: str, error: str) -> None:
        self._history.append({"event": event, "error": error})

class WildcardEventBus(EventBus):
    def __init__(self):
        super().__init__()
        self._wildcards: List[tuple] = []

    def subscribe_pattern(self, pattern: str, handler: Callable) -> None:
        self._wildcards.append((pattern, handler))

    def publish(self, event: str, data: Any = None) -> int:
        count = super().publish(event, data)
        for pattern, handler in self._wildcards:
            if self._matches(pattern, event):
                try:
                    handler(event, data)
                    count += 1
                except Exception:
                    pass
        return count

    def _matches(self, pattern: str, event: str) -> bool:
        if pattern.endswith("*"):
            return event.startswith(pattern[:-1])
        return pattern == event
