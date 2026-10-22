"""limiter_burst: token bucket burst limiter."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """make bucket"""
    import time
        return {"t": cap, "cap": cap, "rate": rate, "last": time.monotonic()}

def allow(*args: Any, **kwargs: Any) -> Any:
    """try consume"""
    import time
        now = time.monotonic()
        b["t"] = min(b["cap"], b["t"] + (now-b["last"])*b["rate"])
        b["last"] = now
        if b["t"] >= 1:
            b["t"] -= 1; return True
        return False

def refill(*args: Any, **kwargs: Any) -> Any:
    """force refill"""
    b["t"] = b["cap"]

__all__ = ["make", "allow", "refill"]
