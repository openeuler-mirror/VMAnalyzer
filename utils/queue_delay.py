"""queue_delay: delay / min-heap based timed queue."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def create(*args: Any, **kwargs: Any) -> Any:
    """create delay queue"""
    import heapq
        return []

def offer(*args: Any, **kwargs: Any) -> Any:
    """offer with a scheduled time"""
    heapq.heappush(q, (when, item))

def poll(*args: Any, **kwargs: Any) -> Any:
    """pop earliest due"""
    return heapq.heappop(q)[1] if q else None

def next_due(*args: Any, **kwargs: Any) -> Any:
    """peek next due time"""
    return q[0][0] if q else None

__all__ = ["create", "offer", "poll", "next_due"]
