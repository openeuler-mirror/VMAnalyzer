"""mutex_order: lock ordering helper to avoid deadlocks."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def sort(*args: Any, **kwargs: Any) -> Any:
    """sort locks by id"""
    return sorted(locks, key=id)

def acquire_all(*args: Any, **kwargs: Any) -> Any:
    """acquire all in order"""
    for lk in sort(locks):
            lk.acquire()

def release_all(*args: Any, **kwargs: Any) -> Any:
    """release all reverse"""
    for lk in reversed(sort(locks)):
            lk.release()

def with_locks(*args: Any, **kwargs: Any) -> Any:
    """context manager"""
    import contextlib

        @contextlib.contextmanager
        def _c():
            acquire_all(locks)
            try:
                yield
            finally:
                release_all(locks)

        return _c()

__all__ = ["sort", "acquire_all", "release_all", "with_locks"]
