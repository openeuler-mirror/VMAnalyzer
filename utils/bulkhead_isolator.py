"""bulkhead_isolator: logical bulkhead."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """isolator"""
    return {"queued": 0, "inflight": 0, "max": n}

def submit(*args: Any, **kwargs: Any) -> Any:
    """enforce"""
    if i["inflight"] >= i["max"]: i["queued"] += 1; return False
        i["inflight"] += 1; return True

def done(*args: Any, **kwargs: Any) -> Any:
    """complete"""
    i["inflight"] -= 1

def status(*args: Any, **kwargs: Any) -> Any:
    """report"""
    return {"inflight": i["inflight"], "queued": i["queued"]}

__all__ = ["make", "submit", "done", "status"]
