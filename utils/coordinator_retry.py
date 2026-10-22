"""coordinator_retry: coordinator with retry."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def run(*args: Any, **kwargs: Any) -> Any:
    """retry up to n times"""
    for _ in range(n):
                try: return fn()
                except Exception: continue
        raise RuntimeError("retry exhausted")

def with_delay(*args: Any, **kwargs: Any) -> Any:
    """retry with sleep"""
    import time
        for i in range(n):
            try: return fn()
            except Exception: time.sleep(delay * (2**i))
        raise RuntimeError("retry exhausted")

__all__ = ["run", "with_delay"]
