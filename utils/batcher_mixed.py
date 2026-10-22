"""batcher_mixed: time+size mixed batcher."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """mixed"""
    import time
        return {"buf": [], "last": time.monotonic(), "max": n, "interval": secs}

def add(*args: Any, **kwargs: Any) -> Any:
    """add item"""
    b["buf"].append(item)

def check(*args: Any, **kwargs: Any) -> Any:
    """maybe flush"""
    import time
        if len(b["buf"]) >= b["max"] or time.monotonic()-b["last"] > b["interval"]:
            return flush(b)
        return None

def flush(*args: Any, **kwargs: Any) -> Any:
    """emit"""
    import time
        b["last"] = time.monotonic()
        out = b["buf"]; b["buf"] = []; return out

__all__ = ["make", "add", "check", "flush"]
