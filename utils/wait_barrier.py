"""wait_barrier: multi-turn barrier."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """create barrier"""
    import threading
        return {"n": part, "count": 0, "lk": threading.Lock(), "ev": threading.Event()}

def arrive(*args: Any, **kwargs: Any) -> Any:
    """arrive at barrier"""
    with b["lk"]:
            b["count"] += 1
            if b["count"] >= b["n"]:
                b["ev"].set()

def wait(*args: Any, **kwargs: Any) -> Any:
    """wait for all"""
    b["ev"].wait()

def reset(*args: Any, **kwargs: Any) -> Any:
    """reset for next round"""
    with b["lk"]:
                b["count"] = 0; b["ev"].clear()

__all__ = ["make", "arrive", "wait", "reset"]
