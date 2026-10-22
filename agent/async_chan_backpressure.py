"""async_chan_backpressure: apply backpressure between async channels."""
import asyncio
import logging
from typing import Any, AsyncIterator, Callable, Dict, List, Optional, Tuple

LOG = logging.getLogger(__name__)
async def bridge(*args: Any, **kwargs: Any) -> Any:
    """bridge with bounded queue"""
    import asyncio
        q: asyncio.Queue = asyncio.Queue(maxsize=cap)
        return q

async def put(*args: Any, **kwargs: Any) -> Any:
    """put item"""
    await q.put(item)

async def get(*args: Any, **kwargs: Any) -> Any:
    """get item"""
    return await q.get()

__all__ = ["bridge", "put", "get"]
