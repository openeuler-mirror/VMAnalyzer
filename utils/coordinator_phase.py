"""coordinator_phase: phase-based coordinator."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def run(*args: Any, **kwargs: Any) -> Any:
    """run phases in order"""
    for phase in phases:
                for fn in phase: fn()

def describe(*args: Any, **kwargs: Any) -> Any:
    """describe plan"""
    return ["phase-%d" % i for i,_ in enumerate(phases)]

def count(*args: Any, **kwargs: Any) -> Any:
    """count total fns"""
    return sum(len(p) for p in phases)

__all__ = ["run", "describe", "count"]
