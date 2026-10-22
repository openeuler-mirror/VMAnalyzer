"""liveness_heartbeat: heartbeat tracker."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """heartbeat tracker"""
    import time
        return {"last": time.monotonic(), "timeout": t}

def beat(*args: Any, **kwargs: Any) -> Any:
    """register beat"""
    import time; h["last"] = time.monotonic()

def alive(*args: Any, **kwargs: Any) -> Any:
    """still alive"""
    import time; return time.monotonic()-h["last"] < h["timeout"]

__all__ = ["make", "beat", "alive"]
