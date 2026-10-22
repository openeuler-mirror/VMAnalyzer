"""deadline_hard: hard deadline with TimeoutError."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def run(*args: Any, **kwargs: Any) -> Any:
    """run until hard deadline"""
    import time
        start = time.monotonic()
        while True:
            if time.monotonic() - start > secs: raise TimeoutError
            if fn(): return True

def or_timeout(*args: Any, **kwargs: Any) -> Any:
    """call with deadline"""
    import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
            f = ex.submit(fn); return f.result(timeout=secs)

__all__ = ["run", "or_timeout"]
