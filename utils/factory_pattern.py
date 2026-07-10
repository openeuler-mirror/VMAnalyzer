#!/usr/bin/env python3
"""Factory pattern for creating shape objects."""
from typing import Dict, Type, Any
from abc import ABC, abstractmethod
import math

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...
    @abstractmethod
    def perimeter(self) -> float: ...
    @abstractmethod
    def describe(self) -> str: ...

class Circle(Shape):
    def __init__(self, radius: float):
        self._radius = radius
    def area(self) -> float:
        return math.pi * self._radius ** 2
    def perimeter(self) -> float:
        return 2 * math.pi * self._radius
    def describe(self) -> str:
        return f"Circle(r={self._radius})"

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self._w = width
        self._h = height
    def area(self) -> float:
        return self._w * self._h
    def perimeter(self) -> float:
        return 2 * (self._w + self._h)
    def describe(self) -> str:
        return f"Rectangle({self._w}x{self._h})"

class Triangle(Shape):
    def __init__(self, a: float, b: float, c: float):
        self._a, self._b, self._c = a, b, c
    def area(self) -> float:
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self._a) * (s - self._b) * (s - self._c))
    def perimeter(self) -> float:
        return self._a + self._b + self._c
    def describe(self) -> str:
        return f"Triangle({self._a},{self._b},{self._c})"

class ShapeFactory:
    _registry: Dict[str, Type] = {"circle": Circle, "rectangle": Rectangle, "triangle": Triangle}
    @classmethod
    def create(cls, shape_type: str, *args) -> Shape:
        if shape_type not in cls._registry:
            raise ValueError(f"Unknown shape: {shape_type}")
        return cls._registry[shape_type](*args)
    @classmethod
    def register(cls, name: str, klass: Type) -> None:
        cls._registry[name] = klass
