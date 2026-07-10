#!/usr/bin/env python3
"""Command pattern with undo/redo support."""
from typing import Any, List, Callable
from collections import deque

class Command:
    def execute(self) -> Any: pass
    def undo(self) -> None: pass

class LambdaCommand(Command):
    def __init__(self, do: Callable, undo_fn: Callable = None):
        self._do = do
        self._undo = undo_fn or (lambda: None)
    def execute(self): return self._do()
    def undo(self): self._undo()

class CommandHistory:
    def __init__(self, max_size: int = 100):
        self._undo_stack: List[Command] = []
        self._redo_stack: List[Command] = []
        self._max_size = max_size

    def execute(self, cmd: Command) -> Any:
        result = cmd.execute()
        self._undo_stack.append(cmd)
        self._redo_stack.clear()
        if len(self._undo_stack) > self._max_size:
            self._undo_stack.pop(0)
        return result

    def undo(self) -> bool:
        if not self._undo_stack:
            return False
        cmd = self._undo_stack.pop()
        cmd.undo()
        self._redo_stack.append(cmd)
        return True

    def redo(self) -> bool:
        if not self._redo_stack:
            return False
        cmd = self._redo_stack.pop()
        cmd.execute()
        self._undo_stack.append(cmd)
        return True

    def can_undo(self) -> bool:
        return bool(self._undo_stack)

    def can_redo(self) -> bool:
        return bool(self._redo_stack)

    def clear(self) -> None:
        self._undo_stack.clear()
        self._redo_stack.clear()
