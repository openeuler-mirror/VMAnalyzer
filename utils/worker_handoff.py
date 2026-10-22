"""worker_handoff: handoff between threads."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """start pool workers"""
    import threading
        def _run(): ...
        threads=[threading.Thread(target=_run, daemon=True) for _ in range(n)]
        [t.start() for t in threads]; return threads

def submit(*args: Any, **kwargs: Any) -> Any:
    """put job"""
    queue.put(job)

def drain(*args: Any, **kwargs: Any) -> Any:
    """drain queue"""
    while not queue.empty(): queue.get()

def stop(*args: Any, **kwargs: Any) -> Any:
    """put poison and join"""
    queue.put(None); [t.join() for t in threads]

__all__ = ["make", "submit", "drain", "stop"]
