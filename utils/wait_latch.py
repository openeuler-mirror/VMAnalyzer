"""wait_latch: one-shot barrier latch."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """create latch"""
    import threading
        return {"ev": threading.Event()}

def release(*args: Any, **kwargs: Any) -> Any:
    """open latch"""
    l["ev"].set()

def await_latched(*args: Any, **kwargs: Any) -> Any:
    """wait until open"""
    l["ev"].wait()

def is_open(*args: Any, **kwargs: Any) -> Any:
    """is open yet"""
    return l["ev"].is_set()

__all__ = ["make", "release", "await_latched", "is_open"]
