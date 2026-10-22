"""worker_drainer: worker that drains queue on stop."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def start(*args: Any, **kwargs: Any) -> Any:
    """start background drainer"""
    import threading, queue
        q = queue.Queue()
        th = threading.Thread(target=lambda: [work(q.get()) for _ in iter(q.get, None)], daemon=True)
        th.start(); return q, th

def submit(*args: Any, **kwargs: Any) -> Any:
    """enqueue"""
    q.put(job)

def stop(*args: Any, **kwargs: Any) -> Any:
    """poison"""
    q.put(None); th.join()

__all__ = ["start", "submit", "stop"]
