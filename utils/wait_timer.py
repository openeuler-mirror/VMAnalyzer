"""wait_timer: high resolution wait timer."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """make timer"""
    import time
        return {"start": time.monotonic()}

def elapsed(*args: Any, **kwargs: Any) -> Any:
    """return seconds"""
    import time; return time.monotonic()-t["start"]

def sleep_ms(*args: Any, **kwargs: Any) -> Any:
    """sleep n ms"""
    import time; time.sleep(ms/1000.0)

def reset(*args: Any, **kwargs: Any) -> Any:
    """reset start"""
    import time; t["start"] = time.monotonic()

__all__ = ["make", "elapsed", "sleep_ms", "reset"]
