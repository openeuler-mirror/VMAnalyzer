"""orchestr_parallel: parallel orchestration."""
import logging
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)
def run(*args: Any, **kwargs: Any) -> Any:
    """run in parallel"""
    import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(fns)) as ex:
            return list(ex.map(lambda f: f(), fns))

def first(*args: Any, **kwargs: Any) -> Any:
    """first succeed"""
    import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(fns)) as ex:
            futs = [ex.submit(f) for f in fns]
            for fut in concurrent.futures.as_completed(futs):
                try: return fut.result()
                except Exception: continue
        return None

def all_ok(*args: Any, **kwargs: Any) -> Any:
    """all succeed"""
    try:
            run(fns); return True
        except Exception: return False

__all__ = ["run", "first", "all_ok"]
