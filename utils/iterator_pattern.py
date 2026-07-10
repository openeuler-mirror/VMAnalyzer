#!/usr/bin/env python3
"""Iterator pattern for custom collection traversal."""
from typing import Any, List, Optional, Callable, Iterator
from abc import ABC, abstractmethod

class CustomIterator(ABC):
    @abstractmethod
    def has_next(self) -> bool: ...
    @abstractmethod
    def next(self) -> Any: ...
    @abstractmethod
    def reset(self) -> None: ...
    @abstractmethod
    def current(self) -> Any: ...

class ListIterator(CustomIterator):
    def __init__(self, data: List[Any]):
        self._data = list(data)
        self._index = 0

    def has_next(self) -> bool:
        return self._index < len(self._data)

    def next(self) -> Any:
        if not self.has_next():
            raise StopIteration("No more elements")
        item = self._data[self._index]
        self._index += 1
        return item

    def reset(self) -> None:
        self._index = 0

    def current(self) -> Any:
        if 0 <= self._index < len(self._data):
            return self._data[self._index]
        return None

class FilterIterator(CustomIterator):
    def __init__(self, data: List[Any], predicate: Callable[[Any], bool]):
        self._data = [item for item in data if predicate(item)]
        self._index = 0

    def has_next(self) -> bool:
        return self._index < len(self._data)

    def next(self) -> Any:
        if not self.has_next():
            raise StopIteration("No more elements")
        item = self._data[self._index]
        self._index += 1
        return item

    def reset(self) -> None:
        self._index = 0

    def current(self) -> Any:
        if 0 <= self._index < len(self._data):
            return self._data[self._index]
        return None

class MapIterator(CustomIterator):
    def __init__(self, data: List[Any], transform: Callable[[Any], Any]):
        self._data = [transform(item) for item in data]
        self._index = 0

    def has_next(self) -> bool:
        return self._index < len(self._data)

    def next(self) -> Any:
        if not self.has_next():
            raise StopIteration("No more elements")
        item = self._data[self._index]
        self._index += 1
        return item

    def reset(self) -> None:
        self._index = 0

    def current(self) -> Any:
        if 0 <= self._index < len(self._data):
            return self._data[self._index]
        return None

class TreeIterator(CustomIterator):
    def __init__(self, root: Any):
        self._stack: List[Any] = []
        if root:
            self._stack.append(root)
        self._current: Any = None

    def has_next(self) -> bool:
        return len(self._stack) > 0

    def next(self) -> Any:
        if not self.has_next():
            raise StopIteration("No more elements")
        node = self._stack.pop()
        self._current = node
        if hasattr(node, "right") and node.right:
            self._stack.append(node.right)
        if hasattr(node, "left") and node.left:
            self._stack.append(node.left)
        return node

    def reset(self) -> None:
        self._stack.clear()
        if self._current:
            self._stack.append(self._current)

    def current(self) -> Any:
        return self._current

class IterableCollection:
    def __init__(self):
        self._items: List[Any] = []

    def add(self, item: Any) -> None:
        self._items.append(item)

    def remove(self, item: Any) -> bool:
        if item in self._items:
            self._items.remove(item)
            return True
        return False

    def create_iterator(self) -> ListIterator:
        return ListIterator(self._items)

    def create_filter_iterator(self, predicate: Callable) -> FilterIterator:
        return FilterIterator(self._items, predicate)

    def create_map_iterator(self, transform: Callable) -> MapIterator:
        return MapIterator(self._items, transform)

    def __iter__(self) -> Iterator:
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def get(self, index: int) -> Any:
        if 0 <= index < len(self._items):
            return self._items[index]
        raise IndexError("Index out of range")
