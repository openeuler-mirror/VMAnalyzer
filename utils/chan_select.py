"""chan_select: select-like fan-in/fan-out."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def merge(*args: Any, **kwargs: Any) -> Any:
    """merge many channels into one"""
    return {"q": [c for ch in channels for c in ch["q"]]}

def split(*args: Any, **kwargs: Any) -> Any:
    """split channel into n clones"""
    return [{"q": list(ch["q"])} for _ in range(n)]

def len_chan(*args: Any, **kwargs: Any) -> Any:
    """return pending count"""
    return len(ch["q"])

def drain(*args: Any, **kwargs: Any) -> Any:
    """drain and return all"""
    out = list(ch["q"]); ch["q"].clear(); return out

__all__ = ["merge", "split", "len_chan", "drain"]
