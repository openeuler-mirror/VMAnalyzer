"""atomic_bool: volatile-like atomic bool."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """make atomic bool"""
    import threading
        return {"v": init, "lk": threading.Lock()}

def compare_exchange(*args: Any, **kwargs: Any) -> Any:
    """conditional update"""
    with b["lk"]:
            if b["v"] == expected:
                b["v"] = target; return True
            return False

def load(*args: Any, **kwargs: Any) -> Any:
    """load current"""
    with b["lk"]:
            return b["v"]

def store(*args: Any, **kwargs: Any) -> Any:
    """store new"""
    with b["lk"]:
            b["v"] = value

__all__ = ["make", "compare_exchange", "load", "store"]
