"""pool_process: process pool wrapper."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """create process pool"""
    import concurrent.futures
        return concurrent.futures.ProcessPoolExecutor(max_workers=n)

def submit(*args: Any, **kwargs: Any) -> Any:
    """submit callable"""
    return p.submit(fn, *args, **kw)

def map(*args: Any, **kwargs: Any) -> Any:
    """map over iterable"""
    return list(p.map(fn, iterable))

def shutdown(*args: Any, **kwargs: Any) -> Any:
    """wait and close"""
    p.shutdown(wait=True)

__all__ = ["make", "submit", "map", "shutdown"]
