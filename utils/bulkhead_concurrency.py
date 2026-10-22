"""bulkhead_concurrency: concurrency bulkhead."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """concurrency limiter"""
    import threading
        return {"lck": threading.Lock(), "active": 0, "max": n}

def enter(*args: Any, **kwargs: Any) -> Any:
    """bump active"""
    with b["lck"]:
            if b["active"] >= b["max"]: return False
            b["active"] += 1; return True

def leave(*args: Any, **kwargs: Any) -> Any:
    """drop"""
    with b["lck"]: b["active"] -= 1

__all__ = ["make", "enter", "leave"]
