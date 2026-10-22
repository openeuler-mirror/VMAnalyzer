"""bulkhead_pool: bulkhead via resource pool."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """bulkhead"""
    import threading
        return {"sem": threading.Semaphore(n), "rejects": 0}

def enter(*args: Any, **kwargs: Any) -> Any:
    """claim"""
    if not b["sem"].acquire(blocking=False):
            b["rejects"] += 1; return False
        return True

def leave(*args: Any, **kwargs: Any) -> Any:
    """release"""
    b["sem"].release()

def stats(*args: Any, **kwargs: Any) -> Any:
    """report"""
    return {"rejects": b["rejects"]}

__all__ = ["make", "enter", "leave", "stats"]
