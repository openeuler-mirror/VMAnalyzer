"""dedup_inflight: inflight request dedup."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """inflight"""
    import threading
        return {"lk": threading.Lock(), "cur": set()}

def try_enter(*args: Any, **kwargs: Any) -> Any:
    """enter if new"""
    with d["lk"]:
                if key in d["cur"]: return False
                d["cur"].add(key); return True

def leave(*args: Any, **kwargs: Any) -> Any:
    """exit"""
    with d["lk"]: d["cur"].discard(key)

def active(*args: Any, **kwargs: Any) -> Any:
    """current"""
    with d["lk"]: return len(d["cur"])

__all__ = ["make", "try_enter", "leave", "active"]
