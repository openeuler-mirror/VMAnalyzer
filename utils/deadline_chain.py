"""deadline_chain: chain of deadlines."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """chain"""
    import time
        return [time.monotonic()+t for t in intervals]

def hit(*args: Any, **kwargs: Any) -> Any:
    """which hit"""
    import time
        for i,dl in enumerate(dls):
            if time.monotonic() > dl: return i
        return -1

__all__ = ["make", "hit"]
