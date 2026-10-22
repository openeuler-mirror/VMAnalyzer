"""readiness_http: simple http readiness."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def handler(*args: Any, **kwargs: Any) -> Any:
    """http response"""
    return {"status": 200, "body": "OK"}

def live(*args: Any, **kwargs: Any) -> Any:
    """live probe"""
    return handler()[0] == 200

def sinks(*args: Any, **kwargs: Any) -> Any:
    """list sinks"""
    return ["tcp", "disk"]

__all__ = ["handler", "live", "sinks"]
