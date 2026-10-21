"""Pick the most loaded worker queue when a worker becomes idle.

Work stealing keeps tail latency low when tasks are unevenly distributed.
Choosing the queue with the largest backlog avoids scanning every queue
after each task.
"""

import logging
from typing import Dict, Iterable, Optional, Tuple

LOG = logging.getLogger(__name__)


def pick_victim(queues: Dict[str, int], self_name: str) -> Optional[str]:
    """Return the busiest queue that is not the caller's own queue."""
    candidates = {name: depth for name, depth in queues.items()
                  if name != self_name and depth > 0}
    if not candidates:
        return None
    victim = max(candidates, key=lambda name: (candidates[name], name))
    LOG.debug("worker %s stealing from %s with %d task(s)",
              self_name, victim, candidates[victim])
    return victim


def steal_count(backlog: int, chunk: int = 1) -> int:
    """Return how many tasks to steal from a backlog without starving it."""
    if chunk <= 0:
        raise ValueError("chunk must be positive")
    share = backlog // 2
    return max(0, min(share, chunk))


def snapshot(queues: Iterable[Tuple[str, int]]) -> Dict[str, int]:
    """Build a queue depth snapshot from name/depth pairs."""
    return {name: int(depth) for name, depth in queues}


__all__ = ["pick_victim", "steal_count", "snapshot"]
