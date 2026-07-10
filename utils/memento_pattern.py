#!/usr/bin/env python3
"""Memento pattern for state capture and restoration."""
from typing import Any, List, Dict

class EditorMemento:
    def __init__(self, content: str, cursor: int, selections: List[tuple]):
        self._content = content
        self._cursor = cursor
        self._selections = list(selections)
        self._timestamp = 0

    def get_content(self) -> str:
        return self._content

    def get_cursor(self) -> int:
        return self._cursor

    def get_selections(self) -> List[tuple]:
        return list(self._selections)

class TextEditor:
    def __init__(self):
        self._content = ""
        self._cursor = 0
        self._selections: List[tuple] = []

    def type(self, text: str) -> None:
        self._content = self._content[:self._cursor] + text + self._content[self._cursor:]
        self._cursor += len(text)

    def move_cursor(self, pos: int) -> None:
        self._cursor = max(0, min(pos, len(self._content)))

    def select(self, start: int, end: int) -> None:
        self._selections.append((start, end))

    def delete_selection(self) -> None:
        if not self._selections:
            return
        start, end = self._selections.pop()
        self._content = self._content[:start] + self._content[end:]
        if self._cursor > end:
            self._cursor -= (end - start)
        elif self._cursor > start:
            self._cursor = start

    def save(self) -> EditorMemento:
        return EditorMemento(self._content, self._cursor, self._selections)

    def restore(self, memento: EditorMemento) -> None:
        self._content = memento.get_content()
        self._cursor = memento.get_cursor()
        self._selections = memento.get_selections()

    @property
    def content(self) -> str:
        return self._content

class History:
    def __init__(self, max_size: int = 50):
        self._stack: List[EditorMemento] = []
        self._max = max_size

    def push(self, memento: EditorMemento) -> None:
        self._stack.append(memento)
        if len(self._stack) > self._max:
            self._stack.pop(0)

    def pop(self) -> EditorMemento:
        if not self._stack:
            raise IndexError("No history")
        return self._stack.pop()

    def size(self) -> int:
        return len(self._stack)

    def clear(self) -> None:
        self._stack.clear()
