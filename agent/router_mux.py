"""router_mux: header/mux router."""
import asyncio
import logging
from typing import Any, AsyncIterator, Callable, Dict, List, Optional, Tuple

LOG = logging.getLogger(__name__)
async def route(*args: Any, **kwargs: Any) -> Any:
    """route by header"""
    table = mux.get(header)
        if table is None: return await default(*a, **k)
        handler = table.get(value, default)
        return await handler(*a, **k)

async def add(*args: Any, **kwargs: Any) -> Any:
    """add entry"""
    mux.setdefault(h, {})[v] = handler

__all__ = ["route", "add"]
