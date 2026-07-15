#!/usr/bin/env python3
"""Socket wrapper with automatic reconnection and retry."""
import socket
import time
from typing import Optional

class SocketWrapper:
    """Wraps a socket with auto-reconnect on failure."""

    def __init__(self, host: str, port: int, timeout: float = 10.0,
                 max_retries: int = 3):
        self._host = host
        self._port = port
        self._timeout = timeout
        self._max_retries = max_retries
        self._sock: Optional[socket.socket] = None

    def connect(self) -> bool:
        """Establish connection with retry logic."""
        for attempt in range(self._max_retries):
            try:
                self._sock = socket.create_connection(
                    (self._host, self._port), self._timeout)
                return True
            except (socket.error, OSError):
                time.sleep(1 + attempt)
        return False

    def send(self, data: bytes) -> int:
        """Send data with auto-reconnect."""
        for _ in range(self._max_retries):
            try:
                return self._sock.send(data)
            except (socket.error, AttributeError):
                if self.connect():
                    continue
        return 0

    def recv(self, size: int = 4096) -> bytes:
        """Receive data."""
        try:
            return self._sock.recv(size)
        except (socket.error, AttributeError):
            return b""

    def close(self) -> None:
        """Close the connection."""
        if self._sock:
            self._sock.close()
            self._sock = None
