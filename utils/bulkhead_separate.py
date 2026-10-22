"""bulkhead_separate: separate pools bulkhead."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """pool dict"""
    return {}

def register(*args: Any, **kwargs: Any) -> Any:
    """add pool"""
    pools[name] = make(max)

def use(*args: Any, **kwargs: Any) -> Any:
    """submit named"""
    return pools[name].submit(fn)

def list(*args: Any, **kwargs: Any) -> Any:
    """list names"""
    return list(pools.keys())

__all__ = ["make", "register", "use", "list"]
