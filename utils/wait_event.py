"""wait_event: condvar-style waitable event."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """create event"""
    import threading
        return threading.Event()

def set(*args: Any, **kwargs: Any) -> Any:
    """set event"""
    ev.set()

def clear(*args: Any, **kwargs: Any) -> Any:
    """clear event"""
    ev.clear()

def wait(*args: Any, **kwargs: Any) -> Any:
    """wait with timeout"""
    return ev.wait(timeout)

__all__ = ["make", "set", "clear", "wait"]
