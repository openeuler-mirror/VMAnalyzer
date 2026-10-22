"""router_dispatch: generic async router."""
import asyncio
import logging
from typing import Any, AsyncIterator, Callable, Dict, List, Optional, Tuple

LOG = logging.getLogger(__name__)
async def register(*args: Any, **kwargs: Any) -> Any:
    """register handler"""
    r[route] = handler

async def dispatch(*args: Any, **kwargs: Any) -> Any:
    """match and call"""
    for pat, h in r.items():
                if pat == key: return await h(*a, **k)
        raise KeyError(key)

async def routes(*args: Any, **kwargs: Any) -> Any:
    """list routes"""
    return list(r.keys())

__all__ = ["register", "dispatch", "routes"]
