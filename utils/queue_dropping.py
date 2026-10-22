"""queue_dropping: queue that drops on overflow."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def create(*args: Any, **kwargs: Any) -> Any:
    """make a dropping queue"""
    from collections import deque
        return deque(maxlen=cap)

def offer(*args: Any, **kwargs: Any) -> Any:
    """offer item, returning True if kept"""
    q.append(item); return True

def poll(*args: Any, **kwargs: Any) -> Any:
    """poll head item"""
    return q.popleft()

def peek(*args: Any, **kwargs: Any) -> Any:
    """peek head"""
    return q[0] if q else None

__all__ = ["create", "offer", "poll", "peek"]
