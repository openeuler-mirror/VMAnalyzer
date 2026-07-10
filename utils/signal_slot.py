#!/usr/bin/env python3
"""Signal/slot mechanism for type-safe component communication."""
from typing import Callable, Any, List, Optional, Dict, Set
import threading
import weakref
from collections import defaultdict

class Signal:
    def __init__(self, *arg_types):
        self._arg_types = arg_types
        self._slots: List[tuple] = []
        self._lock = threading.Lock()
        self._blocked = False
        self._stats = {"emitted": 0, "delivered": 0, "failed": 0}

    def connect(self, slot: Callable, priority: int = 0) -> "Signal":
        with self._lock:
            self._slots.append((priority, slot, True))
            self._slots.sort(key=lambda x: x[0], reverse=True)
        return self

    def connect_once(self, slot: Callable, priority: int = 0) -> "Signal":
        with self._lock:
            self._slots.append((priority, slot, False))
            self._slots.sort(key=lambda x: x[0], reverse=True)
        return self

    def disconnect(self, slot: Callable) -> bool:
        with self._lock:
            for i, (_, s, _) in enumerate(self._slots):
                if s == slot:
                    self._slots.pop(i)
                    return True
            return False

    def emit(self, *args) -> int:
        if self._blocked:
            return 0
        with self._lock:
            slots = list(self._slots)
            to_remove = []
            self._stats["emitted"] += 1
        delivered = 0
        for i, (priority, slot, persistent) in enumerate(slots):
            try:
                slot(*args)
                delivered += 1
                self._stats["delivered"] += 1
            except Exception:
                self._stats["failed"] += 1
            if not persistent:
                to_remove.append(i)
        if to_remove:
            with self._lock:
                for i in reversed(to_remove):
                    if i < len(self._slots):
                        self._slots.pop(i)
        return delivered

    def block(self) -> None:
        self._blocked = True

    def unblock(self) -> None:
        self._blocked = False

    @property
    def is_blocked(self) -> bool:
        return self._blocked

    @property
    def slot_count(self) -> int:
        with self._lock:
            return len(self._slots)

    @property
    def stats(self) -> Dict[str, int]:
        with self._lock:
            return dict(self._stats)

    def clear(self) -> None:
        with self._lock:
            self._slots.clear()

class Slot:
    def __init__(self, func: Callable, name: str = ""):
        self._func = func
        self._name = name or func.__name__
        self._connected_signals: Set[Signal] = set()

    def __call__(self, *args) -> Any:
        return self._func(*args)

    @property
    def name(self) -> str:
        return self._name

    def connect_to(self, signal: Signal, priority: int = 0) -> "Slot":
        signal.connect(self._func, priority)
        self._connected_signals.add(signal)
        return self

    def disconnect_from(self, signal: Signal) -> bool:
        if signal in self._connected_signals:
            signal.disconnect(self._func)
            self._connected_signals.discard(signal)
            return True
        return False

    def disconnect_all(self) -> int:
        count = 0
        for signal in list(self._connected_signals):
            if signal.disconnect(self._func):
                count += 1
        self._connected_signals.clear()
        return count

class SignalBus:
    _instance: Optional["SignalBus"] = None
    _lock = threading.Lock()

    @classmethod
    def instance(cls) -> "SignalBus":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def __init__(self):
        self._signals: Dict[str, Signal] = {}

    def get_signal(self, name: str) -> Signal:
        if name not in self._signals:
            self._signals[name] = Signal()
        return self._signals[name]

    def emit(self, name: str, *args) -> int:
        signal = self._signals.get(name)
        if signal:
            return signal.emit(*args)
        return 0

    def connect(self, name: str, slot: Callable, priority: int = 0) -> Signal:
        return self.get_signal(name).connect(slot, priority)

    def disconnect(self, name: str, slot: Callable) -> bool:
        signal = self._signals.get(name)
        if signal:
            return signal.disconnect(slot)
        return False

    def signal_names(self) -> List[str]:
        return list(self._signals.keys())

    def signal_count(self) -> int:
        return len(self._signals)

    def remove_signal(self, name: str) -> bool:
        if name in self._signals:
            self._signals[name].clear()
            del self._signals[name]
            return True
        return False

    def clear(self) -> None:
        for signal in self._signals.values():
            signal.clear()
        self._signals.clear()
