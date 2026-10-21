"""Priority queue that releases tasks only when their dependencies finish.

Schedulers need to hold tasks whose parents are still running without
rescanning the whole graph every tick.  Tracking dependents per completed
task keeps readiness checks proportional to the affected tasks.
"""

import heapq
import logging
from typing import Dict, Iterable, List, Set, Tuple

LOG = logging.getLogger(__name__)


class ReadyQueue:
    """Track dependencies and expose ready tasks in priority order."""

    def __init__(self) -> None:
        self._dependencies: Dict[str, Set[str]] = {}
        self._dependents: Dict[str, Set[str]] = {}
        self._priority: Dict[str, int] = {}
        self._ready: List[Tuple[int, str]] = []

    def add(self, name: str, priority: int = 0, depends_on: Iterable[str] = ()) -> None:
        """Register a task with its priority and outstanding dependencies."""
        parents = {parent for parent in depends_on if parent in self._dependencies}
        self._dependencies[name] = parents
        self._priority[name] = int(priority)
        for parent in parents:
            self._dependents.setdefault(parent, set()).add(name)
        if not parents:
            heapq.heappush(self._ready, (self._priority[name], name))

    def complete(self, name: str) -> List[str]:
        """Mark a task complete and return tasks that became ready."""
        unlocked: List[str] = []
        for dependent in sorted(self._dependents.get(name, ())):
            parents = self._dependencies.get(dependent, set())
            parents.discard(name)
            if not parents:
                heapq.heappush(self._ready, (self._priority[dependent], dependent))
                unlocked.append(dependent)
        return unlocked

    def pop(self) -> str:
        """Remove and return the highest priority ready task."""
        if not self._ready:
            raise IndexError("no ready task available")
        _, name = heapq.heappop(self._ready)
        return name

    def __len__(self) -> int:
        """Return the number of ready tasks."""
        return len(self._ready)

    def __bool__(self) -> bool:
        """Allow ``if queue`` readiness checks."""
        return bool(self._ready)


__all__ = ["ReadyQueue"]
