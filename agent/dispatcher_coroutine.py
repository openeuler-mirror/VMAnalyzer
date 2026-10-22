"""dispatcher_coroutine: coroutine dispatcher."""
import asyncio
import logging
from typing import Any, AsyncIterator, Callable, Dict, List, Optional, Tuple

LOG = logging.getLogger(__name__)
async def dispatch(*args: Any, **kwargs: Any) -> Any:
    """await all"""
    import asyncio
        return await asyncio.gather(*fns)

async def fanout(*args: Any, **kwargs: Any) -> Any:
    """fanout to all"""
    import asyncio
        return await asyncio.gather(*[f(*a, **k) for f in fns])

async def stop_first(*args: Any, **kwargs: Any) -> Any:
    """return first ok"""
    import asyncio
        for f in asyncio.as_completed([fn(*a, **k) for fn in fns]):
            try: return await f
            except Exception: continue
        return None

__all__ = ["dispatch", "fanout", "stop_first"]
