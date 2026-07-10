#!/usr/bin/env python3
"""Lightweight dependency injection container."""
from typing import Any, Callable, Dict, Type, Optional

class DIContainer:
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, Callable] = {}
        self._singletons: Dict[str, Any] = {}
        self._aliases: Dict[str, str] = {}

    def register(self, name: str, factory: Callable, singleton: bool = True) -> None:
        self._factories[name] = factory
        if singleton:
            self._services[name] = "singleton"
        else:
            self._services[name] = "transient"

    def register_instance(self, name: str, instance: Any) -> None:
        self._singletons[name] = instance
        self._services[name] = "instance"

    def register_alias(self, alias: str, target: str) -> None:
        self._aliases[alias] = target

    def resolve(self, name: str) -> Any:
        if name in self._aliases:
            name = self._aliases[name]

        if name in self._singletons:
            return self._singletons[name]

        if name not in self._factories:
            raise KeyError(f"Service '{name}' not registered")

        instance = self._factories[name](self)

        if self._services.get(name) == "singleton":
            self._singletons[name] = instance

        return instance

    def is_registered(self, name: str) -> bool:
        return name in self._factories or name in self._singletons or name in self._aliases

    def clear(self) -> None:
        self._services.clear()
        self._factories.clear()
        self._singletons.clear()
        self._aliases.clear()
