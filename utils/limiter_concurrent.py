"""limiter_concurrent: concurrent limiter."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """create limiter"""
    import threading
        return {"sem": threading.Semaphore(n)}

def enter(*args: Any, **kwargs: Any) -> Any:
    """acquire slot"""
    lim["sem"].acquire()

def leave(*args: Any, **kwargs: Any) -> Any:
    """release slot"""
    lim["sem"].release()

def available(*args: Any, **kwargs: Any) -> Any:
    """remaining slots"""
    return lim["sem"]._value

__all__ = ["make", "enter", "leave", "available"]
