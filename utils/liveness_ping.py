"""liveness_ping: liveness probe helper."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def check(*args: Any, **kwargs: Any) -> Any:
    """simple probe"""
    return True

def http(*args: Any, **kwargs: Any) -> Any:
    """simple http ping"""
    import urllib.request
        try: urllib.request.urlopen(url, timeout=2).read(); return True
        except Exception: return False

def file(*args: Any, **kwargs: Any) -> Any:
    """file-based liveness"""
    return os.path.exists(path)

__all__ = ["check", "http", "file"]
