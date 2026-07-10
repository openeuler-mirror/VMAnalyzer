#!/usr/bin/env python3
"""Composite pattern for hierarchical tree structures."""
from typing import List, Optional, Any

class Component:
    def __init__(self, name: str):
        self._name = name
        self._parent: Optional["Component"] = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def parent(self) -> Optional["Component"]:
        return self._parent

    def add(self, component: "Component") -> None:
        raise NotImplementedError

    def remove(self, component: "Component") -> None:
        raise NotImplementedError

    def get_children(self) -> List["Component"]:
        return []

    def operation(self) -> str:
        return self._name

    def is_composite(self) -> bool:
        return False

class Leaf(Component):
    def __init__(self, name: str, value: Any = None):
        super().__init__(name)
        self._value = value

    def operation(self) -> str:
        return f"Leaf({self._name}={self._value})"

class Composite(Component):
    def __init__(self, name: str):
        super().__init__(name)
        self._children: List[Component] = []

    def add(self, component: Component) -> None:
        component._parent = self
        self._children.append(component)

    def remove(self, component: Component) -> None:
        component._parent = None
        self._children.remove(component)

    def get_children(self) -> List[Component]:
        return list(self._children)

    def is_composite(self) -> bool:
        return True

    def operation(self) -> str:
        parts = [c.operation() for c in self._children]
        return f"Composite({self._name}: [{', '.join(parts)}])"

    def count(self) -> int:
        count = 0
        for child in self._children:
            if child.is_composite():
                count += child.count()
            else:
                count += 1
        return count
