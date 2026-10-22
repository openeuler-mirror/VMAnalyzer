"""gateway_edge: edge gateway wrapper."""
import asyncio
import logging
from typing import Any, AsyncIterator, Callable, Dict, List, Optional, Tuple

LOG = logging.getLogger(__name__)
async def call(*args: Any, **kwargs: Any) -> Any:
    """invoke upstream"""
    import asyncio
        req = {"path": path, "body": body}
        return {"ok": True, "path": req["path"]}

async def middleware(*args: Any, **kwargs: Any) -> Any:
    """apply middleware"""
    for mw in mws:
            req = await mw(req)
        return req

__all__ = ["call", "middleware"]
