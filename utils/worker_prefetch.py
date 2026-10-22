"""worker_prefetch: prefetching worker."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def run(*args: Any, **kwargs: Any) -> Any:
    """consume items"""
    for item in src: work(item)

def prefetch(*args: Any, **kwargs: Any) -> Any:
    """cache n items"""
    buf=[next(src) for _ in range(n)]; return buf

def flush(*args: Any, **kwargs: Any) -> Any:
    """push remaining"""
    for x in buf: work(x); buf.clear()

__all__ = ["run", "prefetch", "flush"]
