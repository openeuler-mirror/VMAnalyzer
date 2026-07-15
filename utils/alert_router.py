#!/usr/bin/env python3
"""Route alerts to appropriate notification channels."""
from typing import Callable, Dict, List

class AlertRouter:
    """Routes alerts to registered handlers based on severity."""

    def __init__(self):
        self._routes: Dict[str, List[Callable]] = {}
        self._default_handler: Callable = None

    def register(self, severity: str, handler: Callable) -> None:
        """Register a handler for a severity level."""
        if severity not in self._routes:
            self._routes[severity] = []
        self._routes[severity].append(handler)

    def set_default(self, handler: Callable) -> None:
        """Set default handler for unmatched severity."""
        self._default_handler = handler

    def route(self, severity: str, message: str) -> int:
        """Route an alert to registered handlers."""
        handlers = self._routes.get(severity, [])
        if not handlers and self._default_handler:
            handlers = [self._default_handler]
        count = 0
        for handler in handlers:
            try:
                handler(severity, message)
                count += 1
            except Exception:
                pass
        return count

    def list_routes(self) -> Dict[str, int]:
        """Return route summary."""
        return {k: len(v) for k, v in self._routes.items()}
