"""orchestr_sequential: sequential with rollback."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def run(*args: Any, **kwargs: Any) -> Any:
    """run all"""
    for s in steps: s()
        return True

def run_with_rollback(*args: Any, **kwargs: Any) -> Any:
    """run and rollback"""
    executed = []
        try:
            for s, rb in steps:
                s(); executed.append(rb)
            return True
        except Exception:
            for rb in reversed(executed): rb()
            raise

__all__ = ["run", "run_with_rollback"]
