"""readiness_dependency: dependency-based readiness."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """deps tracker"""
    return {name: False for name in names}

def mark(*args: Any, **kwargs: Any) -> Any:
    """mark dep ready"""
    deps[name] = True

def all_ready(*args: Any, **kwargs: Any) -> Any:
    """check all"""
    return all(deps.values())

__all__ = ["make", "mark", "all_ready"]
