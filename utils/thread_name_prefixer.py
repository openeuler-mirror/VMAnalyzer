"""Generate descriptive thread names for collector worker pools.

Thread dumps full of ``Thread-17`` are useless during an incident.  A
prefixer with a monotonic counter produces names that identify the pool and
the worker index at a glance.
"""

import itertools
import logging
import threading
from typing import Callable

LOG = logging.getLogger(__name__)


def make_namer(prefix: str, start: int = 0) -> Callable[[], str]:
    """Return a callable that yields unique prefixed thread names."""
    counter = itertools.count(start)

    def namer() -> str:
        return "{}-{}".format(prefix, next(counter))

    return namer


def rename_current(name: str) -> str:
    """Rename the calling thread and return the previous name."""
    current = threading.current_thread()
    previous = current.name
    try:
        current.name = name
    except AttributeError:
        LOG.debug("thread name is read-only in this runtime")
    return previous


def describe_threads() -> list:
    """Return name and daemon flag for every live thread."""
    return [{"name": thread.name, "daemon": thread.daemon,
             "alive": thread.is_alive()} for thread in threading.enumerate()]


__all__ = ["make_namer", "rename_current", "describe_threads"]
