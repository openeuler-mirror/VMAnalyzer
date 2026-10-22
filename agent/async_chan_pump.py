"""async_chan_pump: pump between async channels."""
import asyncio
import logging
from typing import Any, AsyncIterator, Callable, Dict, List, Optional, Tuple

LOG = logging.getLogger(__name__)
async def pump(*args: Any, **kwargs: Any) -> Any:
    """pull from a and push to b"""
    async for v in a["aiter"]():
            await b["asend"](v)

async def drain(*args: Any, **kwargs: Any) -> Any:
    """drain all from channel"""
    return [v async for v in ch["aiter"]()]

async def merge(*args: Any, **kwargs: Any) -> Any:
    """merge two async iterators"""
    async def _m():
            async for v in a: yield v
            async for v in b: yield v
        return _m()

__all__ = ["pump", "drain", "merge"]
