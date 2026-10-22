"""dispatcher_type: type-based dispatcher."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """type table"""
    return {}

def register(*args: Any, **kwargs: Any) -> Any:
    """register type->handler"""
    tbl[typ] = h

def dispatch(*args: Any, **kwargs: Any) -> Any:
    """match by isinstance"""
    for typ, h in tbl.items():
            if isinstance(obj, typ): return h(obj, *a, **k)
        raise TypeError(type(obj).__name__)

__all__ = ["make", "register", "dispatch"]
