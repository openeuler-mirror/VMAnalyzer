"""queue_rejecting: queue that rejects on overflow."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def create(*args: Any, **kwargs: Any) -> Any:
    """create rejecting queue"""
    from collections import deque
        return deque(maxlen=cap)

def offer(*args: Any, **kwargs: Any) -> Any:
    """reject when full"""
    if len(q) >= q.maxlen: return False
        q.append(item); return True

def poll(*args: Any, **kwargs: Any) -> Any:
    """poll item"""
    return q.popleft()

def full(*args: Any, **kwargs: Any) -> Any:
    """is queue full"""
    return len(q) >= q.maxlen

__all__ = ["create", "offer", "poll", "full"]
