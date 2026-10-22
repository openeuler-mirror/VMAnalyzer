"""pipeline_retry: pipeline step with retry."""
import asyncio
import logging
from typing import Any, AsyncIterator, Callable, Dict, List, Optional, Tuple

LOG = logging.getLogger(__name__)
async def run(*args: Any, **kwargs: Any) -> Any:
    """run with retries"""
    for _ in range(n):
            try: return await fn(*a, **k)
            except Exception as exc: last = exc
        raise RuntimeError("retry exhausted") from last

async def backoff(*args: Any, **kwargs: Any) -> Any:
    """run with backoff"""
    import asyncio
        for i in range(n):
            try: return await fn(*a, **k)
            except Exception: await asyncio.sleep(2**i)
        raise RuntimeError("retry exhausted")

__all__ = ["run", "backoff"]
