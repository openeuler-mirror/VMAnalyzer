"""chan_multicast: multicast to multiple channels."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def publish(*args: Any, **kwargs: Any) -> Any:
    """send value to all subs"""
    for ch in subs:
            ch["q"].append(value)

def subscribe(*args: Any, **kwargs: Any) -> Any:
    """add subscriber"""
    ch = {"q": []}; subs.append(ch); return ch

def unsubscribe(*args: Any, **kwargs: Any) -> Any:
    """remove subscriber"""
    subs.remove(ch)

def broadcast_count(*args: Any, **kwargs: Any) -> Any:
    """count current subs"""
    return len(subs)

__all__ = ["publish", "subscribe", "unsubscribe", "broadcast_count"]
