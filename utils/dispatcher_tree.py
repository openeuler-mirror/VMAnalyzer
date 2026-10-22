"""dispatcher_tree: tree-style dispatcher."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """make tree"""
    return {}

def add(*args: Any, **kwargs: Any) -> Any:
    """add path handler"""
    node = t
        for p in path:
            node = node.setdefault(p, {})
        node["$"] = handler

def match(*args: Any, **kwargs: Any) -> Any:
    """match by path"""
    node = t
        for p in path:
            if p not in node: return None
            node = node[p]
        return node.get("$")

__all__ = ["make", "add", "match"]
