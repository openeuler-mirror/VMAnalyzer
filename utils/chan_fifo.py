"""chan_fifo: python channel-like fifo."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """make a new channel dict"""
    return {"q": [], "closed": False}

def send(*args: Any, **kwargs: Any) -> Any:
    """send value into channel"""
    if ch["closed"]: return False
        ch["q"].append(value); return True

def recv(*args: Any, **kwargs: Any) -> Any:
    """receive from channel"""
    if not ch["q"]: return None
        return ch["q"].pop(0)

def close(*args: Any, **kwargs: Any) -> Any:
    """mark channel closed"""
    ch["closed"] = True

__all__ = ["make", "send", "recv", "close"]
