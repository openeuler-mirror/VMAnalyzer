"""atomic_ref: lock-guarded reference container."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """create ref holder"""
    import threading
        return {"v": value, "lk": threading.RLock()}

def set(*args: Any, **kwargs: Any) -> Any:
    """replace value"""
    with r["lk"]:
            r["v"] = value

def get(*args: Any, **kwargs: Any) -> Any:
    """retrieve value"""
    with r["lk"]:
            return r["v"]

def swap(*args: Any, **kwargs: Any) -> Any:
    """atomic swap"""
    with r["lk"]:
            old = r["v"]; r["v"] = value; return old

__all__ = ["make", "set", "get", "swap"]
