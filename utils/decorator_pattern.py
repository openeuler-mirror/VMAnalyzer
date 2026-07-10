#!/usr/bin/env python3
"""Decorator pattern for extending component behavior."""
from typing import Any, Protocol

class Component(Protocol):
    def operation(self) -> str: ...

class BaseComponent:
    def operation(self) -> str:
        return "base"

class Decorator:
    def __init__(self, component: Component):
        self._component = component

    def operation(self) -> str:
        return self._component.operation()

class UpperCaseDecorator(Decorator):
    def operation(self) -> str:
        return self._component.operation().upper()

class PrefixDecorator(Decorator):
    def __init__(self, component: Component, prefix: str):
        super().__init__(component)
        self._prefix = prefix

    def operation(self) -> str:
        return f"{self._prefix}:{self._component.operation()}"

class SuffixDecorator(Decorator):
    def __init__(self, component: Component, suffix: str):
        super().__init__(component)
        self._suffix = suffix

    def operation(self) -> str:
        return f"{self._component.operation()}:{self._suffix}"

class BracketDecorator(Decorator):
    def operation(self) -> str:
        return f"[{self._component.operation()}]"

class RepeatDecorator(Decorator):
    def __init__(self, component: Component, times: int):
        super().__init__(component)
        self._times = times

    def operation(self) -> str:
        return self._component.operation() * self._times
