#!/usr/bin/env python3
"""Buffered stream processing for chunked data handling."""
from typing import List

class StreamBuffer:
    """Buffers stream data and processes in fixed-size chunks."""

    def __init__(self, chunk_size: int = 4096):
        self._chunk_size = chunk_size
        self._buffer = bytearray()

    def write(self, data: bytes) -> None:
        """Add data to the buffer."""
        self._buffer.extend(data)

    def read_chunk(self) -> bytes:
        """Read and remove one chunk from buffer."""
        if len(self._buffer) < self._chunk_size:
            return b""
        chunk = bytes(self._buffer[:self._chunk_size])
        del self._buffer[:self._chunk_size]
        return chunk

    def read_all(self) -> bytes:
        """Read and clear entire buffer."""
        data = bytes(self._buffer)
        self._buffer.clear()
        return data

    def peek(self, size: int = 0) -> bytes:
        """Peek at buffer contents without consuming."""
        if size:
            return bytes(self._buffer[:size])
        return bytes(self._buffer)

    def available(self) -> int:
        """Return bytes available in buffer."""
        return len(self._buffer)

    def flush(self) -> bytes:
        """Return remaining buffer content and clear."""
        return self.read_all()
