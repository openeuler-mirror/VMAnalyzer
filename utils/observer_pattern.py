#!/usr/bin/env python3
"""Observer pattern with weak references."""
import weakref
from typing import Callable, Any, List

class Subject:
    def __init__(self):
        self._observers: List[weakref.ref] = []

    def attach(self, observer: Any) -> None:
        if hasattr(observer, "update"):
            self._observers.append(weakref.ref(observer))
        elif callable(observer):
            self._observers.append(weakref.WeakMethod(observer))

    def detach(self, observer: Any) -> None:
        ref = weakref.ref(observer) if hasattr(observer, "update") else weakref.WeakMethod(observer)
        if ref in self._observers:
            self._observers.remove(ref)

    def notify(self, *args, **kwargs) -> None:
        dead = []
        for ref in self._observers:
            obs = ref()
            if obs is None:
                dead.append(ref)
            elif callable(obs):
                obs(*args, **kwargs)
            elif hasattr(obs, "update"):
                obs.update(*args, **kwargs)
        for ref in dead:
            self._observers.remove(ref)

class ObservableValue(Subject):
    def __init__(self, value: Any = None):
        super().__init__()
        self._value = value

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, val: Any) -> None:
        old = self._value
        self._value = val
        if old != val:
            self.notify(old, val)

    def get(self) -> Any:
        return self._value
