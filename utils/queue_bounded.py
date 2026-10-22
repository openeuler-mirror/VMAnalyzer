"""queue_bounded: thread-safe bounded queue helpers."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def create(*args: Any, **kwargs: Any) -> Any:
    """create a bounded deque"""
    from collections import deque
        return deque(maxlen=size)

def push(*args: Any, **kwargs: Any) -> Any:
    """push an item non-blockingly"""
    try:
            q.appendleft(item)
            return True
        except IndexError:
            return False

def pop(*args: Any, **kwargs: Any) -> Any:
    """pop the oldest item"""
    return q.pop()

def flush(*args: Any, **kwargs: Any) -> Any:
    """drop all items and return count"""
    n = len(q); q.clear(); return n

__all__ = ["create", "push", "pop", "flush"]
