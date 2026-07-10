#!/usr/bin/env python3
"""Chain of responsibility for request handling."""
from typing import Optional, Any, Dict

class Request:
    def __init__(self, req_type: str, data: Dict[str, Any]):
        self._type = req_type
        self._data = data
        self._handled = False
        self._handler = None

    @property
    def type(self) -> str:
        return self._type

    @property
    def data(self) -> Dict:
        return self._data

    @property
    def handled(self) -> bool:
        return self._handled

    def mark_handled(self, handler: str) -> None:
        self._handled = True
        self._handler = handler

class Handler:
    def __init__(self):
        self._next: Optional[Handler] = None

    def set_next(self, handler: "Handler") -> "Handler":
        self._next = handler
        return handler

    def handle(self, request: Request) -> Optional[Request]:
        if self._next:
            return self._next.handle(request)
        return None

class AuthHandler(Handler):
    def handle(self, request: Request) -> Optional[Request]:
        if request.type == "auth":
            token = request.data.get("token")
            if token and len(token) > 10:
                request.mark_handled("AuthHandler")
                return request
        return super().handle(request)

class LogHandler(Handler):
    def handle(self, request: Request) -> Optional[Request]:
        if request.type == "log":
            level = request.data.get("level", "INFO")
            msg = request.data.get("message", "")
            request.data["formatted"] = f"[{level}] {msg}"
            request.mark_handled("LogHandler")
            return request
        return super().handle(request)

class CacheHandler(Handler):
    def handle(self, request: Request) -> Optional[Request]:
        if request.type == "cache":
            key = request.data.get("key")
            if key:
                request.mark_handled("CacheHandler")
                return request
        return super().handle(request)

class RateLimitHandler(Handler):
    def __init__(self, max_per_minute: int = 100):
        super().__init__()
        self._limit = max_per_minute
        self._counts: Dict[str, int] = {}

    def handle(self, request: Request) -> Optional[Request]:
        if request.type == "api":
            client = request.data.get("client", "default")
            count = self._counts.get(client, 0)
            if count < self._limit:
                self._counts[client] = count + 1
                request.mark_handled("RateLimitHandler")
                return request
            request.data["error"] = "Rate limit exceeded"
        return super().handle(request)
