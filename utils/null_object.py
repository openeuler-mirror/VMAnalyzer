#!/usr/bin/env python3
"""Null object pattern for safe null handling."""
from typing import Any, Optional, Callable, Dict, List
from abc import ABC, abstractmethod

class Logger(ABC):
    @abstractmethod
    def info(self, msg: str) -> None: ...
    @abstractmethod
    def error(self, msg: str) -> None: ...
    @abstractmethod
    def debug(self, msg: str) -> None: ...
    @abstractmethod
    def is_null(self) -> bool: ...

class ConsoleLogger(Logger):
    def info(self, msg: str) -> None:
        print(f"[INFO] {msg}")
    def error(self, msg: str) -> None:
        print(f"[ERROR] {msg}")
    def debug(self, msg: str) -> None:
        print(f"[DEBUG] {msg}")
    def is_null(self) -> bool:
        return False

class NullLogger(Logger):
    def info(self, msg: str) -> None: pass
    def error(self, msg: str) -> None: pass
    def debug(self, msg: str) -> None: pass
    def is_null(self) -> bool:
        return True

class Cache(ABC):
    @abstractmethod
    def get(self, key: str) -> Any: ...
    @abstractmethod
    def set(self, key: str, value: Any) -> None: ...
    @abstractmethod
    def delete(self, key: str) -> bool: ...
    @abstractmethod
    def is_null(self) -> bool: ...

class MemoryCache(Cache):
    def __init__(self):
        self._data: Dict[str, Any] = {}
    def get(self, key: str) -> Any:
        return self._data.get(key)
    def set(self, key: str, value: Any) -> None:
        self._data[key] = value
    def delete(self, key: str) -> bool:
        if key in self._data:
            del self._data[key]
            return True
        return False
    def is_null(self) -> bool:
        return False

class NullCache(Cache):
    def get(self, key: str) -> Any:
        return None
    def set(self, key: str, value: Any) -> None: pass
    def delete(self, key: str) -> bool:
        return False
    def is_null(self) -> bool:
        return True

class Service:
    def __init__(self, logger: Logger = None, cache: Cache = None):
        self._logger = logger or NullLogger()
        self._cache = cache or NullCache()

    def process(self, data: Dict[str, Any]) -> Any:
        self._logger.info("Processing started")
        cached = self._cache.get("result")
        if cached is not None:
            self._logger.debug("Cache hit")
            return cached
        result = self._compute(data)
        self._cache.set("result", result)
        self._logger.info("Processing complete")
        return result

    def _compute(self, data: Dict[str, Any]) -> Any:
        return sum(data.values()) if data else 0

class NullObjectFactory:
    _nulls: Dict[str, Any] = {}

    @classmethod
    def get_null(cls, type_name: str) -> Any:
        if type_name == "logger":
            return NullLogger()
        elif type_name == "cache":
            return NullCache()
        return None

    @classmethod
    def is_null(cls, obj: Any) -> bool:
        if hasattr(obj, "is_null"):
            return obj.is_null()
        return obj is None

    @classmethod
    def coalesce(cls, *objects: Any) -> Any:
        for obj in objects:
            if obj is not None and not cls.is_null(obj):
                return obj
        return None

    @classmethod
    def safe_call(cls, obj: Any, method_name: str, *args, default: Any = None, **kwargs) -> Any:
        if obj is None or cls.is_null(obj):
            return default
        method = getattr(obj, method_name, None)
        if method:
            return method(*args, **kwargs)
        return default
