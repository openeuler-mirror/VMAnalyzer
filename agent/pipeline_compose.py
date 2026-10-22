"""pipeline_compose: compose async pipeline steps."""
import asyncio
import logging
from typing import Any, AsyncIterator, Callable, Dict, List, Optional, Tuple

LOG = logging.getLogger(__name__)
async def compose(*args: Any, **kwargs: Any) -> Any:
    """compose coroutines"""
    async def composed(x):
            for step in steps: x = await step(x)
            return x
        return composed

async def run(*args: Any, **kwargs: Any) -> Any:
    """run composed"""
    return await compose(steps)(initial)

async def trace(*args: Any, **kwargs: Any) -> Any:
    """trace each step"""
    async def traced(x):
            for i,s in enumerate(steps):
                x = await s(x); LOG.info("step %d done", i)
            return x
        return await traced(initial)

__all__ = ["compose", "run", "trace"]
