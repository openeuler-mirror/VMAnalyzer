"""limiter_leaky: leaky bucket limiter."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """leaky bucket"""
    import threading
        return {"q": [], "cap": cap, "rate": rate, "lk": threading.Lock()}

def accept(*args: Any, **kwargs: Any) -> Any:
    """accept if not full"""
    with b["lk"]:
            if len(b["q"]) < b["cap"]:
                b["q"].append(item); return True
            return False

def drip(*args: Any, **kwargs: Any) -> Any:
    """pop oldest"""
    with b["lk"]:
                if b["q"]: b["q"].pop(0)

__all__ = ["make", "accept", "drip"]
