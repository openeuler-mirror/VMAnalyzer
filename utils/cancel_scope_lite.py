"""Coordinate cooperative cancellation across collector sub-tasks.

Threads cannot be killed safely, so cancellation must be cooperative.  A
shared token with parent propagation lets nested work stop promptly without
passing many flags through every call signature.
"""

import logging
import threading
from typing import List, Optional

LOG = logging.getLogger(__name__)


class CancelScope:
    """Cancellation token that can be linked to parent scopes."""

    def __init__(self, parent: Optional["CancelScope"] = None) -> None:
        self._event = threading.Event()
        self._children: List["CancelScope"] = []
        self._parent = parent
        if parent is not None:
            parent._children.append(self)
            if parent.cancelled():
                self._event.set()

    def cancel(self) -> None:
        """Cancel this scope and all of its children."""
        if self._event.is_set():
            return
        self._event.set()
        LOG.debug("cancel scope signalled with %d child scope(s)", len(self._children))
        for child in list(self._children):
            child.cancel()

    def cancelled(self) -> bool:
        """Return True when cancellation has been requested."""
        if self._parent is not None and self._parent.cancelled():
            return True
        return self._event.is_set()

    def sleep(self, seconds: float, step: float = 0.1) -> bool:
        """Sleep in small steps, returning False when cancelled early."""
        remaining = max(0.0, seconds)
        while remaining > 0:
            if self.cancelled():
                return False
            pause = min(step, remaining)
            self._event.wait(pause)
            remaining -= pause
        return not self.cancelled()

    def detach(self) -> None:
        """Remove this scope from its parent's child list."""
        if self._parent is not None:
            self._parent._children.remove(self)
            self._parent = None


__all__ = ["CancelScope"]
