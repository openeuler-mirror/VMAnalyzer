"""dispatcher_round_robin: round-robin dispatcher."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """rr state"""
    return {"handlers": list(h), "idx": 0}

def next(*args: Any, **kwargs: Any) -> Any:
    """pick next"""
    cur = s["handlers"][s["idx"]]
        s["idx"] = (s["idx"] + 1) % len(s["handlers"])
        return cur

def add(*args: Any, **kwargs: Any) -> Any:
    """append handler"""
    s["handlers"].append(h)

def remove(*args: Any, **kwargs: Any) -> Any:
    """remove handler"""
    s["handlers"].remove(h)

__all__ = ["make", "next", "add", "remove"]
