"""queue_unbounded: unbounded fifo queue wrappers."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def create(*args: Any, **kwargs: Any) -> Any:
    """create an unbounded deque"""
    from collections import deque
        return deque()

def enqueue(*args: Any, **kwargs: Any) -> Any:
    """append an item to tail"""
    q.append(item)

def dequeue(*args: Any, **kwargs: Any) -> Any:
    """pop from head"""
    return q.popleft()

def size(*args: Any, **kwargs: Any) -> Any:
    """return current length"""
    return len(q)

__all__ = ["create", "enqueue", "dequeue", "size"]
