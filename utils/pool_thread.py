"""pool_thread: simple thread pool."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """create pool"""
    import concurrent.futures
        return concurrent.futures.ThreadPoolExecutor(max_workers=n)

def submit(*args: Any, **kwargs: Any) -> Any:
    """submit callable"""
    return p.submit(fn, *args, **kw)

def map(*args: Any, **kwargs: Any) -> Any:
    """map over iterable"""
    return list(p.map(fn, iterable))

def shutdown(*args: Any, **kwargs: Any) -> Any:
    """close pool"""
    p.shutdown(wait=True)

__all__ = ["make", "submit", "map", "shutdown"]
