"""coalesce_simple: coalesce consecutive same events."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """coalescer"""
    return {"prev": None, "count": 0}

def push(*args: Any, **kwargs: Any) -> Any:
    """coalesce"""
    if c["prev"] == event:
                c["count"] += 1; return None
        old = (c["prev"], c["count"])
        c["prev"] = event; c["count"] = 1; return old

def flush(*args: Any, **kwargs: Any) -> Any:
    """emit tail"""
    old = (c["prev"], c["count"]); c["prev"] = None; c["count"] = 0; return old

__all__ = ["make", "push", "flush"]
