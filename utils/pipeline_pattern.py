#!/usr/bin/env python3
"""Pipeline pattern for chained data processing."""
from typing import Any, Callable, List, Optional

class PipelineStep:
    def __init__(self, name: str, func: Callable):
        self.name = name
        self.func = func

    def process(self, data: Any) -> Any:
        return self.func(data)

class Pipeline:
    def __init__(self):
        self._steps: List[PipelineStep] = []

    def add_step(self, name: str, func: Callable) -> "Pipeline":
        self._steps.append(PipelineStep(name, func))
        return self

    def remove_step(self, name: str) -> bool:
        for i, step in enumerate(self._steps):
            if step.name == name:
                self._steps.pop(i)
                return True
        return False

    def execute(self, data: Any) -> Any:
        result = data
        for step in self._steps:
            result = step.process(result)
        return result

    def execute_with_trace(self, data: Any) -> dict:
        result = data
        trace = {"input": data, "steps": []}
        for step in self._steps:
            result = step.process(result)
            trace["steps"].append({"name": step.name, "output": result})
        trace["output"] = result
        return trace

    def step_names(self) -> List[str]:
        return [s.name for s in self._steps]

    def insert_after(self, after_name: str, name: str, func: Callable) -> bool:
        for i, step in enumerate(self._steps):
            if step.name == after_name:
                self._steps.insert(i + 1, PipelineStep(name, func))
                return True
        return False
