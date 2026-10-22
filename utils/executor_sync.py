"""executor_sync: synchronous executor."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def submit(*args: Any, **kwargs: Any) -> Any:
    """run immediately"""
    return fn(*args, **kw)

def map(*args: Any, **kwargs: Any) -> Any:
    """map inline"""
    return [fn(x) for x in iterable]

def apply(*args: Any, **kwargs: Any) -> Any:
    """apply tuple"""
    return fn(*args)

def run_all(*args: Any, **kwargs: Any) -> Any:
    """run all callables"""
    return [c() for c in tasks]

__all__ = ["submit", "map", "apply", "run_all"]
