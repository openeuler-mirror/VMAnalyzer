#!/usr/bin/env python3
"""Flyweight pattern for memory-efficient shared objects."""
from typing import Dict, Any, Optional, List

class TreeType:
    def __init__(self, name: str, color: str, texture: str):
        self._name = name
        self._color = color
        self._texture = texture

    @property
    def name(self) -> str:
        return self._name

    @property
    def color(self) -> str:
        return self._color

    @property
    def texture(self) -> str:
        return self._texture

    def render(self, x: int, y: int) -> str:
        return f"{self._name}({self._color}) at ({x},{y})"

class TreeFactory:
    _pool: Dict[str, TreeType] = {}

    @classmethod
    def get_tree_type(cls, name: str, color: str, texture: str) -> TreeType:
        key = f"{name}_{color}_{texture}"
        if key not in cls._pool:
            cls._pool[key] = TreeType(name, color, texture)
        return cls._pool[key]

    @classmethod
    def pool_size(cls) -> int:
        return len(cls._pool)

    @classmethod
    def clear(cls) -> None:
        cls._pool.clear()

class Tree:
    def __init__(self, x: int, y: int, tree_type: TreeType):
        self._x = x
        self._y = y
        self._type = tree_type

    def render(self) -> str:
        return self._type.render(self._x, self._y)

class Forest:
    def __init__(self):
        self._trees: List[Tree] = []

    def plant(self, x: int, y: int, name: str, color: str, texture: str) -> None:
        tree_type = TreeFactory.get_tree_type(name, color, texture)
        self._trees.append(Tree(x, y, tree_type))

    def render(self) -> List[str]:
        return [t.render() for t in self._trees]

    def size(self) -> int:
        return len(self._trees)
