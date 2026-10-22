"""coalesce_debounce: debounce within window."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """debounce"""
    import time
        return {"last": 0.0, "wait": secs}

def fire(*args: Any, **kwargs: Any) -> Any:
    """debounce"""
    import time
        now = time.monotonic()
        if now - d["last"] < d["wait"]: return False
        d["last"] = now; return True

def reset(*args: Any, **kwargs: Any) -> Any:
    """reset timer"""
    d["last"] = 0.0

__all__ = ["make", "fire", "reset"]
