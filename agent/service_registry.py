"""service_registry: async service registry."""
import asyncio
import logging
from typing import Any, AsyncIterator, Callable, Dict, List, Optional, Tuple

LOG = logging.getLogger(__name__)
async def register(*args: Any, **kwargs: Any) -> Any:
    """register endpoint"""
    reg[name] = endpoints

async def lookup(*args: Any, **kwargs: Any) -> Any:
    """lookup by name"""
    return reg.get(name, [])

async def unregister(*args: Any, **kwargs: Any) -> Any:
    """remove"""
    reg.pop(name, None)

__all__ = ["register", "lookup", "unregister"]
