"""breaker_metrics: breaker with counters."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """breaker with metrics"""
    return {"ok": 0, "fail": 0, "total": 0, "state": "closed"}

def ok(*args: Any, **kwargs: Any) -> Any:
    """record ok"""
    b["ok"] += 1; b["total"] += 1

def fail(*args: Any, **kwargs: Any) -> Any:
    """record fail"""
    b["fail"] += 1; b["total"] += 1

def failure_rate(*args: Any, **kwargs: Any) -> Any:
    """ratio"""
    return b["fail"]/b["total"] if b["total"] else 0.0

__all__ = ["make", "ok", "fail", "failure_rate"]
