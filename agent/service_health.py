"""service_health: async service health monitor."""
import asyncio
import logging
from typing import Any, AsyncIterator, Callable, Dict, List, Optional, Tuple

LOG = logging.getLogger(__name__)
async def probe(*args: Any, **kwargs: Any) -> Any:
    """run probe"""
    try:
                await fn(); return True
            except Exception: return False

async def loop(*args: Any, **kwargs: Any) -> Any:
    """periodic check"""
    import asyncio
        while True:
            ok = await probe(fn)
            LOG.info("health=%s", ok)
            await asyncio.sleep(interval)

async def once(*args: Any, **kwargs: Any) -> Any:
    """single check"""
    return await probe(fn)

__all__ = ["probe", "loop", "once"]
