"""lock_spin: simple busy spinlock."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """make spinlock"""
    return {"locked": False}

def acquire(*args: Any, **kwargs: Any) -> Any:
    """spin until free"""
    while sl["locked"]: pass
        sl["locked"] = True

def release(*args: Any, **kwargs: Any) -> Any:
    """release"""
    sl["locked"] = False

def is_locked(*args: Any, **kwargs: Any) -> Any:
    """check state"""
    return sl["locked"]

__all__ = ["make", "acquire", "release", "is_locked"]
