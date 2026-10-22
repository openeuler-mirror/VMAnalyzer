"""mutex_reentrant: reentrant mutex wrapper."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """make rlock"""
    import threading
        return threading.RLock()

def enter(*args: Any, **kwargs: Any) -> Any:
    """enter lock"""
    r.acquire()

def leave(*args: Any, **kwargs: Any) -> Any:
    """leave lock"""
    r.release()

def hold_count(*args: Any, **kwargs: Any) -> Any:
    """nesting count"""
    return r._RLock__count

__all__ = ["make", "enter", "leave", "hold_count"]
