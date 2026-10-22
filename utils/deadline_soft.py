"""deadline_soft: soft deadline wrapper."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """soft deadline"""
    import time
        return time.monotonic() + secs

def remaining(*args: Any, **kwargs: Any) -> Any:
    """seconds left"""
    import time; return max(0.0, dl - time.monotonic())

def expired(*args: Any, **kwargs: Any) -> Any:
    """is past"""
    import time; return time.monotonic() > dl

__all__ = ["make", "remaining", "expired"]
