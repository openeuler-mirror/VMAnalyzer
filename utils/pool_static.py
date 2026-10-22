"""pool_static: fixed static pool."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """static pool"""
    import concurrent.futures
        return concurrent.futures.ThreadPoolExecutor(max_workers=n, thread_name_prefix=name)

def call(*args: Any, **kwargs: Any) -> Any:
    """fire-and-forget wrapper"""
    futures.append(p.submit(fn, *a, **k)); return True

def join(*args: Any, **kwargs: Any) -> Any:
    """wait for all futures"""
    for f in futures: f.result()

def stop(*args: Any, **kwargs: Any) -> Any:
    """shutdown"""
    p.shutdown(wait=True)

__all__ = ["make", "call", "join", "stop"]
