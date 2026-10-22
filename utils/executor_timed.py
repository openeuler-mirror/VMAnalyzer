"""executor_timed: executor with per-call timeout."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def run(*args: Any, **kwargs: Any) -> Any:
    """run fn with timeout"""
    import concurrent.futures

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
            f = ex.submit(fn, *args, **kw)
            return f.result(timeout=timeout)

def safe_run(*args: Any, **kwargs: Any) -> Any:
    """return None on timeout"""
    try:
            return run(timeout, fn, *a, **k)
        except Exception:
            return None

def benchmark(*args: Any, **kwargs: Any) -> Any:
    """time call"""
    import time
        s = time.time()
        fn(*args, **kw)
        return time.time() - s

__all__ = ["run", "safe_run", "benchmark"]
