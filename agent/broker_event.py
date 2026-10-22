"""broker_event: async event broker."""
import asyncio
import logging
from typing import Any, AsyncIterator, Callable, Dict, List, Optional, Tuple

LOG = logging.getLogger(__name__)
async def publish(*args: Any, **kwargs: Any) -> Any:
    """publish event"""
    for sub in subs:
                await sub.receive(event)

async def subscribe(*args: Any, **kwargs: Any) -> Any:
    """subscribe"""
    subs.append(sub); return sub

async def unsubscribe(*args: Any, **kwargs: Any) -> Any:
    """unsub"""
    if sub in subs: subs.remove(sub)

__all__ = ["publish", "subscribe", "unsubscribe"]
