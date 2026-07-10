#!/usr/bin/env python3
"""Repository pattern for abstracted data access."""
from typing import Generic, TypeVar, List, Optional, Dict, Any, Callable
from abc import ABC, abstractmethod
from collections import defaultdict
import threading

T = TypeVar("T")

class Entity(Generic[T]):
    def __init__(self, id: T, data: Dict[str, Any]):
        self._id = id
        self._data = dict(data)
        self._version = 1

    @property
    def id(self) -> T:
        return self._id

    @property
    def data(self) -> Dict[str, Any]:
        return dict(self._data)

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value
        self._version += 1

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    @property
    def version(self) -> int:
        return self._version

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self._id, "version": self._version, **self._data}

class Repository(ABC, Generic[T]):
    @abstractmethod
    def find_by_id(self, id: T) -> Optional[Entity]: ...
    @abstractmethod
    def find_all(self) -> List[Entity]: ...
    @abstractmethod
    def save(self, entity: Entity) -> Entity: ...
    @abstractmethod
    def delete(self, id: T) -> bool: ...
    @abstractmethod
    def count(self) -> int: ...

class InMemoryRepository(Repository[T]):
    def __init__(self):
        self._storage: Dict[T, Entity] = {}
        self._lock = threading.Lock()
        self._indexes: Dict[str, Dict[Any, List[T]]] = defaultdict(lambda: defaultdict(list))
        self._listeners: List[Callable] = []

    def find_by_id(self, id: T) -> Optional[Entity]:
        with self._lock:
            return self._storage.get(id)

    def find_all(self) -> List[Entity]:
        with self._lock:
            return list(self._storage.values())

    def find_by(self, field: str, value: Any) -> List[Entity]:
        with self._lock:
            ids = self._indexes.get(field, {}).get(value, [])
            return [self._storage[i] for i in ids if i in self._storage]

    def find_one_by(self, field: str, value: Any) -> Optional[Entity]:
        results = self.find_by(field, value)
        return results[0] if results else None

    def save(self, entity: Entity) -> Entity:
        with self._lock:
            old = self._storage.get(entity.id)
            self._storage[entity.id] = entity
            for key, val in entity.data.items():
                if old and old.get(key) != val:
                    old_ids = self._indexes[key].get(old.get(key), [])
                    if entity.id in old_ids:
                        old_ids.remove(entity.id)
                if val is not None:
                    self._indexes[key][val].append(entity.id)
        self._notify("save", entity)
        return entity

    def delete(self, id: T) -> bool:
        with self._lock:
            entity = self._storage.pop(id, None)
            if entity:
                for key, val in entity.data.items():
                    ids = self._indexes[key].get(val, [])
                    if id in ids:
                        ids.remove(id)
                self._notify("delete", entity)
                return True
            return False

    def delete_all(self) -> int:
        with self._lock:
            count = len(self._storage)
            self._storage.clear()
            self._indexes.clear()
        return count

    def count(self) -> int:
        with self._lock:
            return len(self._storage)

    def add_index(self, field: str) -> None:
        if field not in self._indexes:
            with self._lock:
                for entity in self._storage.values():
                    val = entity.get(field)
                    if val is not None:
                        self._indexes[field][val].append(entity.id)

    def add_listener(self, callback: Callable) -> None:
        self._listeners.append(callback)

    def _notify(self, action: str, entity: Entity) -> None:
        for cb in self._listeners:
            try:
                cb(action, entity)
            except Exception:
                pass

    def query(self, predicate: Callable[[Entity], bool]) -> List[Entity]:
        with self._lock:
            return [e for e in self._storage.values() if predicate(e)]

    def paginate(self, page: int, page_size: int) -> List[Entity]:
        with self._lock:
            items = list(self._storage.values())
            start = (page - 1) * page_size
            return items[start:start + page_size]
