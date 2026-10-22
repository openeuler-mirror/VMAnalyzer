"""mutex_owner: owner-tracking mutex."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """create owned mutex"""
    import threading
        return {"lk": threading.Lock(), "owner": None}

def acquire(*args: Any, **kwargs: Any) -> Any:
    """set owner"""
    m["lk"].acquire(); m["owner"] = ident

def release(*args: Any, **kwargs: Any) -> Any:
    """clear owner"""
    assert m["owner"] == ident; m["owner"] = None; m["lk"].release()

def who(*args: Any, **kwargs: Any) -> Any:
    """return owner"""
    return m["owner"]

__all__ = ["make", "acquire", "release", "who"]
