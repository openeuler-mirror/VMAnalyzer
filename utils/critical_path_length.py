"""Critical path length for a project task network.

Each task has a duration and depends on zero or more predecessors.  The
critical path is the longest chain of dependent tasks by total duration, and
determines the minimum project completion time.
"""

import logging
from collections import defaultdict, deque
from typing import Dict, Iterable, List, Tuple

LOG = logging.getLogger(__name__)

Dependency = Tuple[str, str]


def critical_path_length(durations: Dict[str, float], dependencies: Iterable[Dependency]) -> float:
    """Return the longest duration path through the task network."""
    adjacency: Dict[str, List[str]] = defaultdict(list)
    indegree: Dict[str, int] = {task: 0 for task in durations}
    for predecessor, successor in dependencies:
        adjacency[predecessor].append(successor)
        indegree[successor] = indegree.get(successor, 0) + 1
    queue = deque(task for task, degree in indegree.items() if degree == 0)
    earliest_finish: Dict[str, float] = {}
    for task in queue:
        earliest_finish[task] = durations.get(task, 0.0)
    longest = 0.0
    while queue:
        task = queue.popleft()
        finish = earliest_finish.get(task, 0.0)
        longest = max(longest, finish)
        for successor in adjacency[task]:
            candidate = finish + durations.get(successor, 0.0)
            earliest_finish[successor] = max(earliest_finish.get(successor, 0.0), candidate)
            indegree[successor] -= 1
            if indegree[successor] == 0:
                queue.append(successor)
    LOG.debug("critical path length %.3f", longest)
    return longest


def earliest_starts(durations: Dict[str, float], dependencies: Iterable[Dependency]) -> Dict[str, float]:
    """Return the earliest start time and finish time of every task."""
    adjacency: Dict[str, List[str]] = defaultdict(list)
    indegree: Dict[str, int] = {task: 0 for task in durations}
    for predecessor, successor in dependencies:
        adjacency[predecessor].append(successor)
        indegree[successor] = indegree.get(successor, 0) + 1
    queue = deque(task for task, degree in indegree.items() if degree == 0)
    start: Dict[str, float] = {task: 0.0 for task in queue}
    while queue:
        task = queue.popleft()
        finish = start[task] + durations.get(task, 0.0)
        for successor in adjacency[task]:
            start[successor] = max(start.get(successor, 0.0), finish)
            indegree[successor] -= 1
            if indegree[successor] == 0:
                queue.append(successor)
    return start


def serial_duration(durations: Dict[str, float]) -> float:
    """Return the total duration if every task ran one after another."""
    return sum(durations.values())


__all__ = ["critical_path_length", "earliest_starts", "serial_duration"]
