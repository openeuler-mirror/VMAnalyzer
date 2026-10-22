"""executor_chained: pipeline executor."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def chain(*args: Any, **kwargs: Any) -> Any:
    """compose fns"""
    def composed(x):
            for f in fns: x = f(x)
            return x
        return composed

def pipe(*args: Any, **kwargs: Any) -> Any:
    """feed value"""
    return reduce(lambda a,b: b(a), fns, init)

def parallel(*args: Any, **kwargs: Any) -> Any:
    """run all on value"""
    return [f(x) for f in fns]

__all__ = ["chain", "pipe", "parallel"]
