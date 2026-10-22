"""chan_broadcast: single-consumer broadcast."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def send(*args: Any, **kwargs: Any) -> Any:
    """broadcast one value"""
    for ch in channels: ch["q"].append(value)

def recv_all(*args: Any, **kwargs: Any) -> Any:
    """receive from all"""
    return [ch["q"].pop(0) for ch in channels if ch["q"]]

def clear(*args: Any, **kwargs: Any) -> Any:
    """clear all channels"""
    for ch in channels: ch["q"].clear()

def alive(*args: Any, **kwargs: Any) -> Any:
    """check alive channel count"""
    return sum(1 for ch in channels if not ch.get("closed"))

__all__ = ["send", "recv_all", "clear", "alive"]
