"""worker_one: single worker."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """spawn one worker thread"""
    import threading
        return threading.Thread(target=fn, args=args, daemon=True)

def start(*args: Any, **kwargs: Any) -> Any:
    """start worker"""
    w.start()

def join(*args: Any, **kwargs: Any) -> Any:
    """wait"""
    w.join(timeout=t)

def is_alive(*args: Any, **kwargs: Any) -> Any:
    """alive check"""
    return w.is_alive()

__all__ = ["make", "start", "join", "is_alive"]
