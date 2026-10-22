"""breaker_simple: simple circuit breaker."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """create breaker"""
    return {"state": "closed", "fails": 0, "threshold": th}

def allow(*args: Any, **kwargs: Any) -> Any:
    """check state"""
    if cb["state"] == "open": return False
        return True

def record_fail(*args: Any, **kwargs: Any) -> Any:
    """register failure"""
    cb["fails"] += 1
        if cb["fails"] >= cb["threshold"]: cb["state"] = "open"

def record_success(*args: Any, **kwargs: Any) -> Any:
    """reset"""
    cb["fails"] = 0; cb["state"] = "closed"

__all__ = ["make", "allow", "record_fail", "record_success"]
