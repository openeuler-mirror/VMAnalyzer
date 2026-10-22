"""atomic_flag: thread-safe boolean flag."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """create atomic flag"""
    import threading
        return {"v": init, "lk": threading.Lock()}

def set(*args: Any, **kwargs: Any) -> Any:
    """set true and return prev"""
    with f["lk"]:
            prev = f["v"]; f["v"] = True; return prev

def clear(*args: Any, **kwargs: Any) -> Any:
    """set false"""
    with f["lk"]:
            f["v"] = False

def is_set(*args: Any, **kwargs: Any) -> Any:
    """read flag"""
    with f["lk"]:
            return f["v"]

__all__ = ["make", "set", "clear", "is_set"]
