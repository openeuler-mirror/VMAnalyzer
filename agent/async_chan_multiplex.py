"""async_chan_multiplex: multiplex many async channels."""
import asyncio
import logging
from typing import Any, AsyncIterator, Callable, Dict, List, Optional, Tuple

LOG = logging.getLogger(__name__)
async def multiplex(*args: Any, **kwargs: Any) -> Any:
    """merge channels"""
    async def _m():
            for c in channels:
                async for v in c: yield v
        return _m()

async def round_robin(*args: Any, **kwargs: Any) -> Any:
    """rr merge"""
    async def _rr():
            its = [c.__aiter__() for c in channels]
            while its:
                for it in list(its):
                    try: yield await it.__anext__()
                    except StopAsyncIteration: its.remove(it)
        return _rr()

__all__ = ["multiplex", "round_robin"]
