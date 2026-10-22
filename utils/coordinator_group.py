"""coordinator_group: coordinated group."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def run_all(*args: Any, **kwargs: Any) -> Any:
    """run all members"""
    return [m() for m in members]

def first(*args: Any, **kwargs: Any) -> Any:
    """first ok"""
    for m in members:
                try: return m()
                except Exception: continue
        return None

def race(*args: Any, **kwargs: Any) -> Any:
    """race all"""
    import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(members)) as ex:
            return next(ex.map(lambda m: m(), members))

__all__ = ["run_all", "first", "race"]
