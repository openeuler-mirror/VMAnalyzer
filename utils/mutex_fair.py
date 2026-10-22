"""mutex_fair: fair mutex with FIFO queue."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """make fair mutex"""
    import threading
        return {"lk": threading.Lock(), "cond": threading.Condition(), "queue": []}

def lock(*args: Any, **kwargs: Any) -> Any:
    """enqueue and wait"""
    with fm["cond"]:
                me = object(); fm["queue"].append(me)
                while fm["queue"][0] is not me: fm["cond"].wait()

def unlock(*args: Any, **kwargs: Any) -> Any:
    """pop head"""
    with fm["cond"]:
                fm["queue"].pop(0); fm["cond"].notify_all()

__all__ = ["make", "lock", "unlock"]
