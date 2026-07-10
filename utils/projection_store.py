#!/usr/bin/env python3
"""Projection store for maintaining read-optimized models."""
from typing import Any, Dict, List, Optional, Callable
from collections import defaultdict
import threading
import time

class Projection:
    def __init__(self, name: str, handler: Callable):
        self._name = name
        self._handler = handler
        self._data: Dict[str, Any] = {}
        self._lock = threading.Lock()
        self._last_event_version = 0
        self._stats = {"processed": 0, "errors": 0, "updates": 0}

    @property
    def name(self) -> str:
        return self._name

    @property
    def last_version(self) -> int:
        return self._last_event_version

    def handle(self, event_type: str, event_data: Any, version: int) -> bool:
        with self._lock:
            if version <= self._last_event_version:
                return False
            try:
                self._data = self._handler(self._data, event_type, event_data)
                self._last_event_version = version
                self._stats["processed"] += 1
                self._stats["updates"] += 1
                return True
            except Exception:
                self._stats["errors"] += 1
                return False

    def get(self, key: str, default: Any = None) -> Any:
        with self._lock:
            return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        with self._lock:
            self._data[key] = value

    def query(self, predicate: Callable) -> List[Any]:
        with self._lock:
            if isinstance(self._data, dict):
                return [v for v in self._data.values() if predicate(v)]
            elif isinstance(self._data, list):
                return [v for v in self._data if predicate(v)]
            return []

    def get_all(self) -> Any:
        with self._lock:
            return self._data

    def rebuild(self, events: List[dict]) -> int:
        with self._lock:
            self._data = {}
            self._last_event_version = 0
            self._stats["processed"] = 0
        count = 0
        for event in events:
            if self.handle(event["type"], event["data"], event["version"]):
                count += 1
        return count

    @property
    def stats(self) -> Dict[str, int]:
        with self._lock:
            return dict(self._stats)

    def reset(self) -> None:
        with self._lock:
            self._data = {}
            self._last_event_version = 0

class ProjectionStore:
    def __init__(self):
        self._projections: Dict[str, Projection] = {}
        self._lock = threading.Lock()
        self._global_handlers: Dict[str, List[str]] = defaultdict(list)

    def register(self, projection: Projection,
                 event_types: Optional[List[str]] = None) -> None:
        with self._lock:
            self._projections[projection.name] = projection
            if event_types:
                for et in event_types:
                    self._global_handlers[et].append(projection.name)
            else:
                self._global_handlers["*"].append(projection.name)

    def unregister(self, name: str) -> bool:
        with self._lock:
            if name in self._projections:
                del self._projections[name]
                for et in list(self._global_handlers.keys()):
                    if name in self._global_handlers[et]:
                        self._global_handlers[et].remove(name)
                        if not self._global_handlers[et]:
                            del self._global_handlers[et]
                return True
            return False

    def dispatch(self, event_type: str, event_data: Any, version: int) -> int:
        with self._lock:
            projection_names = set(self._global_handlers.get(event_type, []))
            projection_names.update(self._global_handlers.get("*", []))
            projections = [self._projections[name] for name in projection_names
                          if name in self._projections]
        count = 0
        for projection in projections:
            if projection.handle(event_type, event_data, version):
                count += 1
        return count

    def get_projection(self, name: str) -> Optional[Projection]:
        return self._projections.get(name)

    def list_projections(self) -> List[str]:
        return list(self._projections.keys())

    @property
    def projection_count(self) -> int:
        return len(self._projections)

    def rebuild_all(self, events: List[dict]) -> Dict[str, int]:
        results = {}
        for name, projection in self._projections.items():
            results[name] = projection.rebuild(events)
        return results

    def get_stats(self) -> Dict[str, Dict[str, int]]:
        return {name: p.stats for name, p in self._projections.items()}

    def reset_all(self) -> None:
        for projection in self._projections.values():
            projection.reset()

    def query(self, projection_name: str, predicate: Callable) -> List[Any]:
        projection = self._projections.get(projection_name)
        if projection:
            return projection.query(predicate)
        return []
