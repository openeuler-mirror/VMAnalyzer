"""Gantt-style ordering of tasks by duration and explicit dependencies.

Tasks are described as ``(name, prerequisite, duration)`` triples.  This
module extracts the prerequisite graph, produces a duration-ordered view for
chart rendering, and reports simple aggregate statistics.
"""

import logging
from typing import Dict, List, Sequence, Set, Tuple

LOG = logging.getLogger(__name__)

Task = Tuple[str, str, float]


def explicit_dependencies(tasks: Sequence[Task]) -> Dict[str, Set[str]]:
    """Return ``{task: prerequisites}`` derived from the link column."""
    graph: Dict[str, Set[str]] = {name: set() for name, _, _ in tasks}
    known = set(graph)
    for name, prerequisite, _ in tasks:
        if prerequisite in known and prerequisite != name:
            graph[name].add(prerequisite)
    LOG.debug("resolved dependencies for %d tasks", len(graph))
    return graph


def schedule_lengths(tasks: Sequence[Task]) -> List[Tuple[str, float]]:
    """Return tasks ordered by descending duration for chart layout."""
    return sorted(((name, duration) for name, _, duration in tasks),
                  key=lambda item: (-item[1], item[0]))


def total_duration(tasks: Sequence[Task]) -> float:
    """Return the summed duration column across all tasks."""
    return sum(duration for _, _, duration in tasks)


def unscheduled(tasks: Sequence[Task]) -> List[str]:
    """Return tasks whose prerequisite is not part of the task list."""
    known = {name for name, _, _ in tasks}
    return sorted({name for name, prerequisite, _ in tasks
                   if prerequisite and prerequisite not in known})


__all__ = ["explicit_dependencies", "schedule_lengths", "total_duration", "unscheduled"]
