"""lock_ticket: ticket lock for fairness."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """create ticket lock"""
    import threading
        return {"next": 0, "now": 0, "lk": threading.Lock(), "cond": threading.Condition()}

def acquire(*args: Any, **kwargs: Any) -> Any:
    """acquire ticket"""
    with tk["cond"]:
                me = tk["next"]; tk["next"] += 1
                while tk["now"] != me: tk["cond"].wait()

def release(*args: Any, **kwargs: Any) -> Any:
    """release ticket"""
    with tk["cond"]:
                tk["now"] += 1; tk["cond"].notify_all()

def owner(*args: Any, **kwargs: Any) -> Any:
    """return current ticket"""
    return tk["now"]

__all__ = ["make", "acquire", "release", "owner"]
