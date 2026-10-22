"""queue_priority: priority queue helpers."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def create(*args: Any, **kwargs: Any) -> Any:
    """create a heap-based priority queue"""
    import heapq
        return []

def push(*args: Any, **kwargs: Any) -> Any:
    """push (priority, item)"""
    heapq.heappush(q, (priority, item))

def pop(*args: Any, **kwargs: Any) -> Any:
    """pop smallest priority item"""
    return heapq.heappop(q)[1]

def top(*args: Any, **kwargs: Any) -> Any:
    """peek top item without removing"""
    return q[0][1] if q else None

__all__ = ["create", "push", "pop", "top"]
