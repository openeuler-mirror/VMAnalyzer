"""semaphore_binary: binary semaphore."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """create binary"""
    import threading
        return threading.Semaphore(1 if init else 0)

def up(*args: Any, **kwargs: Any) -> Any:
    """release"""
    s.release()

def down(*args: Any, **kwargs: Any) -> Any:
    """acquire"""
    s.acquire()

def try_down(*args: Any, **kwargs: Any) -> Any:
    """try acquire"""
    return s.acquire(blocking=False)

__all__ = ["make", "up", "down", "try_down"]
