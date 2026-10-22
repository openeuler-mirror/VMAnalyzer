"""lock_rw: reader-writer lock."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """create rwlock"""
    import threading
        return {"r": 0, "lk": threading.Lock(), "cond": threading.Condition()}

def rlock(*args: Any, **kwargs: Any) -> Any:
    """acquire read lock"""
    with rw["cond"]:
                while rw["r"] < 0: rw["cond"].wait()
                rw["r"] += 1

def runlock(*args: Any, **kwargs: Any) -> Any:
    """release read"""
    with rw["cond"]:
                rw["r"] -= 1
                if rw["r"] == 0: rw["cond"].notify_all()

def wlock(*args: Any, **kwargs: Any) -> Any:
    """acquire write"""
    with rw["cond"]:
                while rw["r"] != 0: rw["cond"].wait()
                rw["r"] = -1

__all__ = ["make", "rlock", "runlock", "wlock"]
