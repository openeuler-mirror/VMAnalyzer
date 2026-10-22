"""dedup_set: simple set-based dedup."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """make deduper"""
    return set()

def seen(*args: Any, **kwargs: Any) -> Any:
    """add and return True if new"""
    if x in s: return False
        s.add(x); return True

def clear(*args: Any, **kwargs: Any) -> Any:
    """reset"""
    s.clear()

def size(*args: Any, **kwargs: Any) -> Any:
    """count"""
    return len(s)

__all__ = ["make", "seen", "clear", "size"]
