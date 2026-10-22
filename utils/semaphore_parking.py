"""semaphore_parking: parking semaphore."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """make parking"""
    import threading
        return {"ev": threading.Event()}

def park(*args: Any, **kwargs: Any) -> Any:
    """block until unpark"""
    p["ev"].wait()

def unpark(*args: Any, **kwargs: Any) -> Any:
    """wake parked"""
    p["ev"].set()

def reset(*args: Any, **kwargs: Any) -> Any:
    """re-arm"""
    p["ev"].clear()

__all__ = ["make", "park", "unpark", "reset"]
