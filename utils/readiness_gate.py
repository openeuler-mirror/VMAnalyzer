"""readiness_gate: readiness gate."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def open(*args: Any, **kwargs: Any) -> Any:
    """open gate"""
    g["open"] = True

def close(*args: Any, **kwargs: Any) -> Any:
    """close gate"""
    g["open"] = False

def ready(*args: Any, **kwargs: Any) -> Any:
    """is open"""
    return g.get("open", False)

__all__ = ["open", "close", "ready"]
