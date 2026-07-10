#!/usr/bin/env python3
"""Saga orchestrator for managing distributed transactions."""
from typing import Callable, Any, List, Dict, Optional, Tuple
from enum import Enum
import time
import threading

class SagaState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    COMPENSATING = "compensating"
    FAILED = "failed"
    COMPENSATED = "compensated"

class SagaStep:
    def __init__(self, name: str, action: Callable, compensation: Callable):
        self._name = name
        self._action = action
        self._compensation = compensation
        self._state = SagaState.PENDING
        self._result: Any = None
        self._error: Optional[str] = None
        self._timestamp: Optional[float] = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def state(self) -> SagaState:
        return self._state

    @property
    def result(self) -> Any:
        return self._result

    @property
    def error(self) -> Optional[str]:
        return self._error

    def execute(self, *args, **kwargs) -> Any:
        self._state = SagaState.RUNNING
        self._timestamp = time.time()
        try:
            result = self._action(*args, **kwargs)
            self._result = result
            self._state = SagaState.COMPLETED
            return result
        except Exception as e:
            self._error = str(e)
            self._state = SagaState.FAILED
            raise

    def compensate(self, *args, **kwargs) -> Any:
        self._state = SagaState.COMPENSATING
        try:
            result = self._compensation(*args, **kwargs)
            self._state = SagaState.COMPENSATED
            return result
        except Exception as e:
            self._error = str(e)
            self._state = SagaState.FAILED
            raise

class Saga:
    def __init__(self, name: str = ""):
        self._name = name
        self._steps: List[SagaStep] = []
        self._state = SagaState.PENDING
        self._completed_steps: List[int] = []
        self._lock = threading.Lock()
        self._on_start: Optional[Callable] = None
        self._on_complete: Optional[Callable] = None
        self._on_compensate: Optional[Callable] = None

    def add_step(self, name: str, action: Callable, compensation: Callable) -> "Saga":
        self._steps.append(SagaStep(name, action, compensation))
        return self

    def on_start(self, callback: Callable) -> "Saga":
        self._on_start = callback
        return self

    def on_complete(self, callback: Callable) -> "Saga":
        self._on_complete = callback
        return self

    def on_compensate(self, callback: Callable) -> "Saga":
        self._on_compensate = callback
        return self

    def execute(self, *args, **kwargs) -> Tuple[bool, Any]:
        with self._lock:
            self._state = SagaState.RUNNING
            self._completed_steps = []
        if self._on_start:
            self._on_start(self)
        for i, step in enumerate(self._steps):
            try:
                result = step.execute(*args, **kwargs)
                self._completed_steps.append(i)
            except Exception:
                self._compensate(*args, **kwargs)
                return False, step.error
        self._state = SagaState.COMPLETED
        if self._on_complete:
            self._on_complete(self)
        return True, [s.result for s in self._steps if s.state == SagaState.COMPLETED]

    def _compensate(self, *args, **kwargs) -> None:
        self._state = SagaState.COMPENSATING
        if self._on_compensate:
            self._on_compensate(self)
        for i in reversed(self._completed_steps):
            step = self._steps[i]
            try:
                step.compensate(*args, **kwargs)
            except Exception:
                pass
        self._state = SagaState.COMPENSATED

    @property
    def state(self) -> SagaState:
        return self._state

    @property
    def steps(self) -> List[SagaStep]:
        return list(self._steps)

    def step_count(self) -> int:
        return len(self._steps)

    def completed_step_count(self) -> int:
        return len(self._completed_steps)

class SagaOrchestrator:
    def __init__(self):
        self._sagas: Dict[str, Saga] = {}
        self._lock = threading.Lock()
        self._stats = {"executed": 0, "succeeded": 0, "failed": 0, "compensated": 0}

    def register_saga(self, name: str, saga: Saga) -> None:
        with self._lock:
            self._sagas[name] = saga

    def execute_saga(self, name: str, *args, **kwargs) -> Tuple[bool, Any]:
        saga = self._sagas.get(name)
        if saga is None:
            raise ValueError(f"Saga '{name}' not found")
        with self._lock:
            self._stats["executed"] += 1
        success, result = saga.execute(*args, **kwargs)
        with self._lock:
            if success:
                self._stats["succeeded"] += 1
            else:
                self._stats["failed"] += 1
                self._stats["compensated"] += 1
        return success, result

    def get_saga(self, name: str) -> Optional[Saga]:
        return self._sagas.get(name)

    def list_sagas(self) -> List[str]:
        return list(self._sagas.keys())

    @property
    def stats(self) -> Dict[str, int]:
        with self._lock:
            return dict(self._stats)

    def saga_count(self) -> int:
        return len(self._sagas)
