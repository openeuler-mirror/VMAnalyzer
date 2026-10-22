"""lock_deadline: deadline-aware lock acquire."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def try_acquire(*args: Any, **kwargs: Any) -> Any:
    """acquire with absolute deadline"""
    import time
        start = time.time()
        while True:
            if m.acquire(blocking=False): return True
            if time.time() > deadline: return False
            time.sleep(0.001)

def try_lock(*args: Any, **kwargs: Any) -> Any:
    """non-blocking try"""
    return m.acquire(blocking=False)

def with_timeout(*args: Any, **kwargs: Any) -> Any:
    """context manager wrapper"""
    import contextlib, time

        @contextlib.contextmanager
        def _c():
            try_acquire(m, time.time()+t)
            try:
                yield
            finally:
                m.release()

        return _c()

__all__ = ["try_acquire", "try_lock", "with_timeout"]
