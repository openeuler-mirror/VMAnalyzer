#!/usr/bin/env python3
"""Domain event dispatcher for Domain-Driven Design."""
from typing import Any, Callable, Dict, List, Optional, Set
from collections import defaultdict
import time
import threading
from dataclasses import dataclass, field

@dataclass
class DomainEvent:
    event_id: str
    event_type: str
    aggregate_id: str
    aggregate_type: str
    data: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)
    version: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

class DomainEventHandler:
    def __init__(self, name: str, handler: Callable, priority: int = 0):
        self._name = name
        self._handler = handler
        self._priority = priority
        self._handled_count = 0
        self._error_count = 0

    @property
    def name(self) -> str:
        return self._name

    @property
    def priority(self) -> int:
        return self._priority

    @property
    def handled_count(self) -> int:
        return self._handled_count

    @property
    def error_count(self) -> int:
        return self._error_count

    def handle(self, event: DomainEvent) -> Any:
        try:
            result = self._handler(event)
            self._handled_count += 1
            return result
        except Exception:
            self._error_count += 1
            raise

class DomainEventDispatcher:
    def __init__(self):
        self._handlers: Dict[str, List[DomainEventHandler]] = defaultdict(list)
        self._pre_dispatch: List[Callable] = []
        self._post_dispatch: List[Callable] = []
        self._lock = threading.Lock()
        self._event_log: List[DomainEvent] = []
        self._max_log = 10000

    def register(self, event_type: str, handler: Callable,
                 name: str = "", priority: int = 0) -> DomainEventHandler:
        handler_obj = DomainEventHandler(name or handler.__name__, handler, priority)
        with self._lock:
            self._handlers[event_type].append(handler_obj)
            self._handlers[event_type].sort(key=lambda h: h.priority, reverse=True)
        return handler_obj

    def unregister(self, event_type: str, handler: DomainEventHandler) -> bool:
        with self._lock:
            handlers = self._handlers.get(event_type, [])
            for i, h in enumerate(handlers):
                if h == handler:
                    handlers.pop(i)
                    return True
            return False

    def dispatch(self, event: DomainEvent) -> List[Any]:
        for pre in self._pre_dispatch:
            if not pre(event):
                return []
        with self._lock:
            handlers = list(self._handlers.get(event.event_type, []))
            handlers.extend(self._handlers.get("*", []))
            self._event_log.append(event)
            if len(self._event_log) > self._max_log:
                self._event_log.pop(0)
        results = []
        for handler in handlers:
            try:
                result = handler.handle(event)
                results.append(result)
            except Exception as e:
                results.append({"error": str(e), "handler": handler.name})
        for post in self._post_dispatch:
            post(event, results)
        return results

    def dispatch_async(self, event: DomainEvent) -> threading.Thread:
        t = threading.Thread(target=self.dispatch, args=(event,), daemon=True)
        t.start()
        return t

    def add_pre_dispatch_hook(self, hook: Callable) -> None:
        self._pre_dispatch.append(hook)

    def add_post_dispatch_hook(self, hook: Callable) -> None:
        self._post_dispatch.append(hook)

    def handler_count(self, event_type: str) -> int:
        return len(self._handlers.get(event_type, []))

    def event_types(self) -> List[str]:
        return list(self._handlers.keys())

    def get_event_log(self, event_type: Optional[str] = None,
                      limit: int = 100) -> List[DomainEvent]:
        with self._lock:
            events = list(self._event_log)
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        return events[-limit:]

    def clear_log(self) -> None:
        with self._lock:
            self._event_log.clear()

class AggregateRoot:
    def __init__(self, aggregate_id: str, aggregate_type: str = ""):
        self._aggregate_id = aggregate_id
        self._aggregate_type = aggregate_type or self.__class__.__name__
        self._version = 0
        self._events: List[DomainEvent] = []
        self._dispatcher: Optional[DomainEventDispatcher] = None

    @property
    def aggregate_id(self) -> str:
        return self._aggregate_id

    @property
    def aggregate_type(self) -> str:
        return self._aggregate_type

    @property
    def version(self) -> int:
        return self._version

    def set_dispatcher(self, dispatcher: DomainEventDispatcher) -> None:
        self._dispatcher = dispatcher

    def add_event(self, event_type: str, data: Dict[str, Any],
                  metadata: Optional[Dict] = None) -> DomainEvent:
        self._version += 1
        event = DomainEvent(
            event_id=f"{self._aggregate_id}_{self._version}",
            event_type=event_type,
            aggregate_id=self._aggregate_id,
            aggregate_type=self._aggregate_type,
            data=data,
            version=self._version,
            metadata=metadata or {}
        )
        self._events.append(event)
        self._apply_event(event)
        return event

    def commit(self) -> List[DomainEvent]:
        events = list(self._events)
        if self._dispatcher:
            for event in events:
                self._dispatcher.dispatch(event)
        self._events.clear()
        return events

    def _apply_event(self, event: DomainEvent) -> None:
        pass

    def get_uncommitted_events(self) -> List[DomainEvent]:
        return list(self._events)

    def load_from_history(self, events: List[DomainEvent]) -> None:
        for event in events:
            self._apply_event(event)
            self._version = event.version

    def clear_events(self) -> None:
        self._events.clear()
