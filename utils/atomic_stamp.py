"""atomic_stamp: atomic monotonic stamp."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """create stamp source"""
    import threading
        return {"v": 0, "lk": threading.Lock()}

def next(*args: Any, **kwargs: Any) -> Any:
    """return next stamp"""
    with s["lk"]:
            s["v"] += 1; return s["v"]

def peek(*args: Any, **kwargs: Any) -> Any:
    """peek current"""
    with s["lk"]:
            return s["v"]

def reset(*args: Any, **kwargs: Any) -> Any:
    """reset to zero"""
    with s["lk"]:
            s["v"] = 0

__all__ = ["make", "next", "peek", "reset"]
