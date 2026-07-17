#!/usr/bin/env python3
"""Cancellation token pattern for cooperative task cancellation."""
import threading
from typing import Callable, List

class CancelToken:
    """A cancellation token for cooperative cancellation."""

    def __init__(self):
        self._cancelled = False
        self._condition = threading.Condition()
        self._callbacks: List[Callable] = []

    def cancel(self) -> None:
        """Signal cancellation."""
        with self._condition:
            if not self._cancelled:
                self._cancelled = True
                self._condition.notify_all()
                for cb in self._callbacks:
                    try:
                        cb()
                    except Exception:
                        pass

    def is_cancelled(self) -> bool:
        """Check if cancellation has been requested."""
        return self._cancelled

    def wait(self, timeout: float = None) -> bool:
        """Wait until cancelled."""
        with self._condition:
            if self._cancelled:
                return True
            return self._condition.wait_for(
                lambda: self._cancelled, timeout=timeout)

    def on_cancel(self, callback: Callable) -> None:
        """Register a callback for cancellation."""
        if self._cancelled:
            callback()
        else:
            self._callbacks.append(callback)

    def link(self, other: "CancelToken") -> None:
        """Link this token to cancel when another is cancelled."""
        other.on_cancel(self.cancel)
