#!/usr/bin/env python3
"""Visitor pattern for operations on object structures."""
from typing import List, Any

class Visitor:
    def visit_file(self, element: "FileElement") -> Any:
        pass
    def visit_directory(self, element: "DirectoryElement") -> Any:
        pass
    def visit_link(self, element: "LinkElement") -> Any:
        pass

class Element:
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def accept(self, visitor: Visitor) -> Any:
        raise NotImplementedError

class FileElement(Element):
    def __init__(self, name: str, size: int):
        super().__init__(name)
        self._size = size

    @property
    def size(self) -> int:
        return self._size

    def accept(self, visitor: Visitor) -> Any:
        return visitor.visit_file(self)

class DirectoryElement(Element):
    def __init__(self, name: str):
        super().__init__(name)
        self._children: List[Element] = []

    def add(self, element: Element) -> None:
        self._children.append(element)

    def get_children(self) -> List[Element]:
        return list(self._children)

    def accept(self, visitor: Visitor) -> Any:
        return visitor.visit_directory(self)

class LinkElement(Element):
    def __init__(self, name: str, target: Element):
        super().__init__(name)
        self._target = target

    @property
    def target(self) -> Element:
        return self._target

    def accept(self, visitor: Visitor) -> Any:
        return visitor.visit_link(self)

class SizeCalculatorVisitor(Visitor):
    def __init__(self):
        self._total = 0

    def visit_file(self, element: FileElement) -> Any:
        self._total += element.size

    def visit_directory(self, element: DirectoryElement) -> Any:
        for child in element.get_children():
            child.accept(self)

    def visit_link(self, element: LinkElement) -> Any:
        element.target.accept(self)

    @property
    def total_size(self) -> int:
        return self._total

class ListVisitor(Visitor):
    def __init__(self):
        self._paths: List[str] = []

    def visit_file(self, element: FileElement) -> Any:
        self._paths.append(element.name)

    def visit_directory(self, element: DirectoryElement) -> Any:
        self._paths.append(f"{element.name}/")
        for child in element.get_children():
            child.accept(self)

    def visit_link(self, element: LinkElement) -> Any:
        self._paths.append(f"{element.name} -> {element.target.name}")

    @property
    def paths(self) -> List[str]:
        return self._paths
