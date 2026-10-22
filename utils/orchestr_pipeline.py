"""orchestr_pipeline: pipeline orchestration."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def compose(*args: Any, **kwargs: Any) -> Any:
    """compose steps"""
    def run(*a,**k):
        v = steps[0](*a, **k)
        for s in steps[1:]: v = s(v)
        return v
        return run

def run(*args: Any, **kwargs: Any) -> Any:
    """run pipeline"""
    return compose(steps)(*a, **k)

def with_error(*args: Any, **kwargs: Any) -> Any:
    """error-handled version"""
    try: return compose(steps)(*a, **k)
        except Exception as exc: return default(exc)

__all__ = ["compose", "run", "with_error"]
