#!/usr/bin/env python3
"""Advanced observer pattern with weak references and priorities."""
from typing import Callable, Any, Optional, List, Dict
import weakref
import threading
from enum import IntEnum
from collections import defaultdict

class Priority(IntEnum):
    LOWEST = 0
    LOW = 25
    NORMAL = 50
    HIGH = 75
    HIGHEST = 100

class Event:
    def __init__(self, name: str, data: Any = None, source: Any = None):
        self._name = name
        self._data = data
        self._source = source
        self._propagation_stopped = False
        self._default_prevented = False

    @property
    def name(self) -> str:
        return self._name

    @property
    def data(self) -> Any:
        return self._data

    @property
    def source(self) -> Any:
        return self._source

    def stop_propagation(self) -> None:
        self._propagation_stopped = True

    @property
    def propagation_stopped(self) -> bool:
        return self._propagation_stopped

    def prevent_default(self) -> None:
        self._default_prevented = True

    @property
    def default_prevented(self) -> bool:
        return self._default_prevented

class WeakObserver:
    def __init__(self, callback: Callable, priority: Priority = Priority.NORMAL):
        try:
            self._ref = weakref.WeakMethod(callback) if hasattr(callback, '__self__') else None
        except TypeError:
            self._ref = None
        self._callback = callback if self._ref is None else None
        self._priority = priority

    @property
    def priority(self) -> Priority:
        return self._priority

    def get_callback(self) -> Optional[Callable]:
        if self._ref:
            return self._ref()
        return self._callback

    def is_alive(self) -> bool:
        return self.get_callback() is not None

    def __call__(self, event: Event) -> None:
        cb = self.get_callback()
        if cb:
            cb(event)

class EventEmitter:
    def __init__(self):
        self._observers: Dict[str, List[WeakObserver]] = defaultdict(list)
        self._lock = threading.Lock()
        self._max_listeners = 100
        self._stats = {"emitted": 0, "delivered": 0, "dropped": 0}

    def on(self, event_name: str, callback: Callable,
           priority: Priority = Priority.NORMAL) -> "EventEmitter":
        with self._lock:
            if len(self._observers[event_name]) >= self._max_listeners:
                raise RuntimeError(f"Max listeners ({self._max_listeners}) reached for '{event_name}'")
            observer = WeakObserver(callback, priority)
            self._observers[event_name].append(observer)
            self._observers[event_name].sort(key=lambda o: o.priority, reverse=True)
        return self

    def once(self, event_name: str, callback: Callable,
             priority: Priority = Priority.NORMAL) -> "EventEmitter":
        def wrapper(event: Event):
            self.off(event_name, wrapper)
            callback(event)
        return self.on(event_name, wrapper, priority)

    def off(self, event_name: str, callback: Callable) -> bool:
        with self._lock:
            observers = self._observers.get(event_name, [])
            for i, obs in enumerate(observers):
                if obs.get_callback() == callback or obs._callback == callback:
                    observers.pop(i)
                    return True
            return False

    def emit(self, event_name: str, data: Any = None, source: Any = None) -> int:
        event = Event(event_name, data, source)
        with self._lock:
            observers = list(self._observers.get(event_name, []))
            alive = [o for o in observers if o.is_alive()]
            dead = [o for o in observers if not o.is_alive()]
            if dead:
                self._observers[event_name] = alive
            self._stats["emitted"] += 1
        delivered = 0
        for observer in alive:
            if event.propagation_stopped:
                break
            try:
                observer(event)
                delivered += 1
                self._stats["delivered"] += 1
            except Exception:
                self._stats["dropped"] += 1
        return delivered

    def emit_async(self, event_name: str, data: Any = None, source: Any = None) -> None:
        threading.Thread(target=self.emit, args=(event_name, data, source), daemon=True).start()

    def remove_all_listeners(self, event_name: Optional[str] = None) -> int:
        with self._lock:
            if event_name:
                count = len(self._observers.get(event_name, []))
                self._observers.pop(event_name, None)
                return count
            else:
                count = sum(len(v) for v in self._observers.values())
                self._observers.clear()
                return count

    def listener_count(self, event_name: str) -> int:
        with self._lock:
            return len([o for o in self._observers.get(event_name, []) if o.is_alive()])

    def event_names(self) -> List[str]:
        with self._lock:
            return [name for name, obs in self._observers.items() if any(o.is_alive() for o in obs)]

    def set_max_listeners(self, max_count: int) -> None:
        self._max_listeners = max_count

    @property
    def stats(self) -> Dict[str, int]:
        with self._lock:
            return dict(self._stats)
