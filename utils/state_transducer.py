"""state_transducer: event transducer state machine."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def make(*args: Any, **kwargs: Any) -> Any:
    """build fsm"""
    return {"state": start, "trans": trans}

def step(*args: Any, **kwargs: Any) -> Any:
    """advance"""
    if event not in m["trans"].get(m["state"], {}): return None
        m["state"] = m["trans"][m["state"]][event]
        return m["state"]

def current(*args: Any, **kwargs: Any) -> Any:
    """current state"""
    return m["state"]

__all__ = ["make", "step", "current"]
