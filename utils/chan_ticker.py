"""chan_ticker: periodic ticker channel."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def start(*args: Any, **kwargs: Any) -> Any:
    """record start time"""
    import time; return {"t": time.time()}

def elapsed(*args: Any, **kwargs: Any) -> Any:
    """ms since start"""
    import time; return int((time.time()-ch["t"])*1000)

def reset(*args: Any, **kwargs: Any) -> Any:
    """reset clock"""
    import time; ch["t"] = time.time()

def stop(*args: Any, **kwargs: Any) -> Any:
    """mark ticker stopped"""
    ch["stopped"] = True

__all__ = ["start", "elapsed", "reset", "stop"]
