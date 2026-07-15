#!/usr/bin/env python3
"""Thread-local context management for per-thread state."""
import threading
from typing import Any, Dict, Optional

class ThreadLocalContext:
    """Manages per-thread context variables."""

    def __init__(self):
        self._local = threading.local()

    def set(self, key: str, value: Any) -> None:
        """Set a context variable for current thread."""
        if not hasattr(self._local, "ctx"):
            self._local.ctx = {}
        self._local.ctx[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get a context variable for current thread."""
        if not hasattr(self._local, "ctx"):
            return default
        return self._local.ctx.get(key, default)

    def delete(self, key: str) -> bool:
        """Delete a context variable."""
        if hasattr(self._local, "ctx") and key in self._local.ctx:
            del self._local.ctx[key]
            return True
        return False

    def clear(self) -> None:
        """Clear all context for current thread."""
        if hasattr(self._local, "ctx"):
            self._local.ctx.clear()

    def all(self) -> Dict[str, Any]:
        """Return all context variables for current thread."""
        return dict(getattr(self._local, "ctx", {}))
