"""dispatcher_keyed: keyed dispatcher."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """create dispatcher"""
    return {}

def register(*args: Any, **kwargs: Any) -> Any:
    """register handler"""
    d[key] = handler

def dispatch(*args: Any, **kwargs: Any) -> Any:
    """dispatch by key"""
    if key in d: return d[key](*a, **k)
        raise KeyError(key)

def keys(*args: Any, **kwargs: Any) -> Any:
    """list keys"""
    return list(d.keys())

__all__ = ["make", "register", "dispatch", "keys"]
