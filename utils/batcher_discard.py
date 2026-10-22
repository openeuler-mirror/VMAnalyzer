"""batcher_discard: batcher that discards on overflow."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """discard"""
    return {"buf": [], "max": n, "discarded": 0}

def add(*args: Any, **kwargs: Any) -> Any:
    """drop if full"""
    if len(b["buf"]) >= b["max"]:
            b["discarded"] += 1; return False
        b["buf"].append(item); return True

def stats(*args: Any, **kwargs: Any) -> Any:
    """report"""
    return {"kept": len(b["buf"]), "discarded": b["discarded"]}

__all__ = ["make", "add", "stats"]
