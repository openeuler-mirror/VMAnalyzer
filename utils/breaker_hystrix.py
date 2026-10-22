"""breaker_hystrix: hystrix-like breaker."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """hystrix breaker"""
    return {"closed_fails": 0, "state": "closed"}

def allow(*args: Any, **kwargs: Any) -> Any:
    """enter"""
    return b["state"] != "open"

def short_circuit(*args: Any, **kwargs: Any) -> Any:
    """open"""
    b["state"] = "open"

def reset(*args: Any, **kwargs: Any) -> Any:
    """close"""
    b["state"] = "closed"; b["closed_fails"] = 0

__all__ = ["make", "allow", "short_circuit", "reset"]
