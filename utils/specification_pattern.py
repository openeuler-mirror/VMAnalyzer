#!/usr/bin/env python3
"""Specification pattern for composable business rules."""
from typing import TypeVar, Generic, Any, List, Callable
from abc import ABC, abstractmethod

T = TypeVar("T")

class Specification(ABC, Generic[T]):
    @abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool: ...

    def and_(self, other: "Specification[T]") -> "Specification[T]":
        return AndSpecification(self, other)

    def or_(self, other: "Specification[T]") -> "Specification[T]":
        return OrSpecification(self, other)

    def not_(self) -> "Specification[T]":
        return NotSpecification(self)

class AndSpecification(Specification[T]):
    def __init__(self, *specs: Specification[T]):
        self._specs = specs

    def is_satisfied_by(self, candidate: T) -> bool:
        return all(spec.is_satisfied_by(candidate) for spec in self._specs)

class OrSpecification(Specification[T]):
    def __init__(self, *specs: Specification[T]):
        self._specs = specs

    def is_satisfied_by(self, candidate: T) -> bool:
        return any(spec.is_satisfied_by(candidate) for spec in self._specs)

class NotSpecification(Specification[T]):
    def __init__(self, spec: Specification[T]):
        self._spec = spec

    def is_satisfied_by(self, candidate: T) -> bool:
        return not self._spec.is_satisfied_by(candidate)

class LambdaSpecification(Specification[T]):
    def __init__(self, predicate: Callable[[T], bool]):
        self._predicate = predicate

    def is_satisfied_by(self, candidate: T) -> bool:
        return self._predicate(candidate)

class SpecificationBuilder:
    @staticmethod
    def field_equals(field_name: str, value: Any) -> Specification:
        return LambdaSpecification(lambda obj: getattr(obj, field_name, None) == value)

    @staticmethod
    def field_greater_than(field_name: str, value: Any) -> Specification:
        return LambdaSpecification(lambda obj: getattr(obj, field_name, 0) > value)

    @staticmethod
    def field_less_than(field_name: str, value: Any) -> Specification:
        return LambdaSpecification(lambda obj: getattr(obj, field_name, 0) < value)

    @staticmethod
    def field_in(field_name: str, values: List[Any]) -> Specification:
        return LambdaSpecification(lambda obj: getattr(obj, field_name, None) in values)

    @staticmethod
    def field_contains(field_name: str, substring: str) -> Specification:
        return LambdaSpecification(
            lambda obj: substring in str(getattr(obj, field_name, ""))
        )

    @staticmethod
    def always_true() -> Specification:
        return LambdaSpecification(lambda obj: True)

    @staticmethod
    def always_false() -> Specification:
        return LambdaSpecification(lambda obj: False)

class SpecificationRepository:
    def __init__(self):
        self._items: List[Any] = []
        self._specs: Dict[str, Specification] = {}

    def add(self, item: Any) -> None:
        self._items.append(item)

    def add_all(self, items: List[Any]) -> None:
        self._items.extend(items)

    def find(self, spec: Specification) -> List[Any]:
        return [item for item in self._items if spec.is_satisfied_by(item)]

    def find_one(self, spec: Specification) -> Any:
        for item in self._items:
            if spec.is_satisfied_by(item):
                return item
        return None

    def count(self, spec: Specification) -> int:
        return sum(1 for item in self._items if spec.is_satisfied_by(item))

    def exists(self, spec: Specification) -> bool:
        return any(spec.is_satisfied_by(item) for item in self._items)

    def register_spec(self, name: str, spec: Specification) -> None:
        self._specs[name] = spec

    def get_spec(self, name: str) -> Specification:
        return self._specs.get(name)

    def remove(self, spec: Specification) -> int:
        before = len(self._items)
        self._items = [item for item in self._items if not spec.is_satisfied_by(item)]
        return before - len(self._items)

    @property
    def size(self) -> int:
        return len(self._items)
