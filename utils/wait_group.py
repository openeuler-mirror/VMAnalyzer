"""wait_group: WaitGroup implementation."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """create waitgroup"""
    import threading
        return {"c": 0, "lk": threading.Lock(), "ev": threading.Event()}

def add(*args: Any, **kwargs: Any) -> Any:
    """delta adder"""
    with wg["lk"]:
            wg["c"] += delta
            if wg["c"] <= 0:
                wg["ev"].set()

def done(*args: Any, **kwargs: Any) -> Any:
    """equivalent to add(-1)"""
    add(wg, -1)

def wait(*args: Any, **kwargs: Any) -> Any:
    """block until zero"""
    with wg["lk"]:
                if wg["c"] <= 0: return
            wg["ev"].wait()

__all__ = ["make", "add", "done", "wait"]
