"""lock_mutex: simple mutex wrapper."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """create mutex"""
    import threading
        return threading.Lock()

def acquire(*args: Any, **kwargs: Any) -> Any:
    """acquire mutex"""
    return m.acquire(timeout=timeout)

def release(*args: Any, **kwargs: Any) -> Any:
    """release mutex"""
    m.release()

def with_lock(*args: Any, **kwargs: Any) -> Any:
    """context manager helper"""
    import contextlib

        @contextlib.contextmanager
        def _ctx():
            m.acquire()
            try:
                yield
            finally:
                m.release()

        return _ctx()

__all__ = ["make", "acquire", "release", "with_lock"]
