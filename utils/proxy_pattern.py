#!/usr/bin/env python3
"""Proxy pattern for controlled access to resources."""
from typing import Any, Dict, Optional

class DataService:
    def __init__(self):
        self._data: Dict[str, Any] = {}
        self._access_count = 0

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value

    def get(self, key: str) -> Optional[Any]:
        self._access_count += 1
        return self._data.get(key)

    def delete(self, key: str) -> bool:
        if key in self._data:
            del self._data[key]
            return True
        return False

    def keys(self) -> list:
        return list(self._data.keys())

class ProtectedProxy:
    def __init__(self, service: DataService, allowed_users: set):
        self._service = service
        self._allowed = allowed_users
        self._current_user = None

    def authenticate(self, user: str) -> bool:
        if user in self._allowed:
            self._current_user = user
            return True
        return False

    def get(self, key: str) -> Optional[Any]:
        if self._current_user is None:
            raise PermissionError("Not authenticated")
        return self._service.get(key)

    def set(self, key: str, value: Any) -> None:
        if self._current_user is None:
            raise PermissionError("Not authenticated")
        self._service.set(key, value)

class CachingProxy:
    def __init__(self, service: DataService):
        self._service = service
        self._cache: Dict[str, Any] = {}
        self._hits = 0
        self._misses = 0

    def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            self._hits += 1
            return self._cache[key]
        self._misses += 1
        val = self._service.get(key)
        if val is not None:
            self._cache[key] = val
        return val

    def stats(self) -> Dict[str, int]:
        return {"hits": self._hits, "misses": self._misses}

    def invalidate(self, key: str = None) -> None:
        if key:
            self._cache.pop(key, None)
        else:
            self._cache.clear()
