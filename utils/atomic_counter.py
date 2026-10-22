"""atomic_counter: thread-safe integer counter."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """create atomic counter"""
    import threading
        return {"v": init, "lk": threading.Lock()}

def inc(*args: Any, **kwargs: Any) -> Any:
    """increment by n"""
    with c["lk"]:
            c["v"] += n; return c["v"]

def dec(*args: Any, **kwargs: Any) -> Any:
    """decrement by n"""
    with c["lk"]:
            c["v"] -= n; return c["v"]

def get(*args: Any, **kwargs: Any) -> Any:
    """read value"""
    with c["lk"]:
            return c["v"]

__all__ = ["make", "inc", "dec", "get"]
