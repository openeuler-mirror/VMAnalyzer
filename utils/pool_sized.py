"""pool_sized: bounded pool that queues tasks."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """sized pool"""
    import concurrent.futures
        return concurrent.futures.ThreadPoolExecutor(max_workers=n)

def run(*args: Any, **kwargs: Any) -> Any:
    """run and block for result"""
    return pool.submit(fn, *a, **k).result(timeout=t)

def stats(*args: Any, **kwargs: Any) -> Any:
    """return dummy stats"""
    return {"max": n, "active": 0}

def close(*args: Any, **kwargs: Any) -> Any:
    """close with drain"""
    pool.shutdown(wait=True, cancel_futures=False)

__all__ = ["make", "run", "stats", "close"]
