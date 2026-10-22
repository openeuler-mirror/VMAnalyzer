"""coalesce_throttle: throttle events."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """throttle"""
    import time
        return {"last": 0.0, "min_delta": secs}

def allow(*args: Any, **kwargs: Any) -> Any:
    """allow if enough gap"""
    import time
        now = time.monotonic()
        if now - t["last"] >= t["min_delta"]:
            t["last"] = now; return True
        return False

def reset(*args: Any, **kwargs: Any) -> Any:
    """reset baseline"""
    t["last"] = 0.0

__all__ = ["make", "allow", "reset"]
