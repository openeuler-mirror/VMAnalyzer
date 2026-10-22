"""pipeline_broadcast: broadcast across pipeline branches."""
import asyncio
import logging
from typing import Any, AsyncIterator, Callable, Dict, List, Optional, Tuple

LOG = logging.getLogger(__name__)
async def broadcast(*args: Any, **kwargs: Any) -> Any:
    """run all branches"""
    import asyncio
        return await asyncio.gather(*[b(x) for b in branches])

async def first(*args: Any, **kwargs: Any) -> Any:
    """first succeed"""
    import asyncio
        for f in asyncio.as_completed([b(x) for b in branches]):
            try: return await f
            except Exception: continue
        return None

__all__ = ["broadcast", "first"]
