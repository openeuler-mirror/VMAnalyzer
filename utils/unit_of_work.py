#!/usr/bin/env python3
"""Unit of work pattern for transactional operations."""
from typing import Dict, List, Any, Optional, Callable, Set
import threading
from enum import Enum

class OperationType(Enum):
    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"

class Operation:
    def __init__(self, op_type: OperationType, entity_type: str,
                 entity_id: Any, data: Optional[Dict] = None):
        self._type = op_type
        self._entity_type = entity_type
        self._entity_id = entity_id
        self._data = data or {}
        self._timestamp = threading.get_ident()

    @property
    def type(self) -> OperationType:
        return self._type

    @property
    def entity_type(self) -> str:
        return self._entity_type

    @property
    def entity_id(self) -> Any:
        return self._entity_id

    @property
    def data(self) -> Dict:
        return dict(self._data)

    def __repr__(self) -> str:
        return f"Op({self._type.value}, {self._entity_type}:{self._entity_id})"

class UnitOfWork:
    def __init__(self):
        self._operations: List[Operation] = []
        self._snapshots: Dict[str, Dict[Any, Any]] = {}
        self._lock = threading.Lock()
        self._active = False
        self._committed = False
        self._rolled_back = False
        self._hooks_before_commit: List[Callable] = []
        self._hooks_after_commit: List[Callable] = []
        self._hooks_rollback: List[Callable] = []

    @property
    def is_active(self) -> bool:
        return self._active

    @property
    def is_committed(self) -> bool:
        return self._committed

    @property
    def is_rolled_back(self) -> bool:
        return self._rolled_back

    def begin(self) -> None:
        self._active = True
        self._committed = False
        self._rolled_back = False
        self._operations.clear()
        self._snapshots.clear()

    def register_insert(self, entity_type: str, entity_id: Any, data: Dict) -> None:
        if not self._active:
            raise RuntimeError("UoW not active")
        with self._lock:
            self._operations.append(Operation(OperationType.INSERT, entity_type, entity_id, data))

    def register_update(self, entity_type: str, entity_id: Any, data: Dict,
                        old_data: Optional[Dict] = None) -> None:
        if not self._active:
            raise RuntimeError("UoW not active")
        with self._lock:
            if old_data:
                key = f"{entity_type}:{entity_id}"
                self._snapshots[key] = old_data
            self._operations.append(Operation(OperationType.UPDATE, entity_type, entity_id, data))

    def register_delete(self, entity_type: str, entity_id: Any,
                        old_data: Optional[Dict] = None) -> None:
        if not self._active:
            raise RuntimeError("UoW not active")
        with self._lock:
            if old_data:
                key = f"{entity_type}:{entity_id}"
                self._snapshots[key] = old_data
            self._operations.append(Operation(OperationType.DELETE, entity_type, entity_id))

    def add_before_commit_hook(self, hook: Callable) -> None:
        self._hooks_before_commit.append(hook)

    def add_after_commit_hook(self, hook: Callable) -> None:
        self._hooks_after_commit.append(hook)

    def add_rollback_hook(self, hook: Callable) -> None:
        self._hooks_rollback.append(hook)

    def commit(self, executor: Optional[Callable[[List[Operation]], None]] = None) -> None:
        if not self._active:
            raise RuntimeError("UoW not active")
        if self._committed:
            raise RuntimeError("UoW already committed")
        for hook in self._hooks_before_commit:
            hook(self._operations)
        if executor:
            executor(list(self._operations))
        self._committed = True
        self._active = False
        for hook in self._hooks_after_commit:
            hook(self._operations)

    def rollback(self) -> None:
        if not self._active:
            raise RuntimeError("UoW not active")
        for hook in self._hooks_rollback:
            hook(self._operations, self._snapshots)
        self._rolled_back = True
        self._active = False

    @property
    def operations(self) -> List[Operation]:
        return list(self._operations)

    @property
    def operation_count(self) -> int:
        return len(self._operations)

    def get_changes(self, entity_type: Optional[str] = None) -> List[Operation]:
        if entity_type:
            return [op for op in self._operations if op.entity_type == entity_type]
        return list(self._operations)

    def get_affected_ids(self) -> Set[Any]:
        return {op.entity_id for op in self._operations}

    def clear(self) -> None:
        self._operations.clear()
        self._snapshots.clear()
        self._active = False
        self._committed = False
        self._rolled_back = False
