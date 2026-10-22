"""executor_async: asyncio executor helper."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """create asyncio loop"""
    import asyncio
        return asyncio.new_event_loop()

def run(*args: Any, **kwargs: Any) -> Any:
    """run coro"""
    return loop.run_until_complete(coro)

def close(*args: Any, **kwargs: Any) -> Any:
    """close loop"""
    loop.close()

def is_running(*args: Any, **kwargs: Any) -> Any:
    """check loop state"""
    return loop.is_running()

__all__ = ["make", "run", "close", "is_running"]
