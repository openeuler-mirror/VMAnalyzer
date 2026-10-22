"""dedup_bloom: bloom-like dedup."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """bloom"""
    return {"bits": [False]*cap, "hashes": hashes}

def seen(*args: Any, **kwargs: Any) -> Any:
    """maybe seen"""
    idx = sum(hash(x) % len(b["bits"]) for _ in range(b["hashes"])) % len(b["bits"])
        if b["bits"][idx]: return True
        b["bits"][idx] = True; return False

def clear(*args: Any, **kwargs: Any) -> Any:
    """reset"""
    b["bits"] = [False]*len(b["bits"])

__all__ = ["make", "seen", "clear"]
