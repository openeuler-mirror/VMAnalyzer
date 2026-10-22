"""semaphore_quick: quick counting semaphore."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """create semaphore"""
    import threading
        return threading.Semaphore(n)

def acquire(*args: Any, **kwargs: Any) -> Any:
    """decrement"""
    s.acquire()

def release(*args: Any, **kwargs: Any) -> Any:
    """increment"""
    s.release(n)

def available(*args: Any, **kwargs: Any) -> Any:
    """approx available"""
    return s._value

__all__ = ["make", "acquire", "release", "available"]
