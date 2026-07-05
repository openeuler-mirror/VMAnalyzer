"""Collection error type model."""

from __future__ import annotations

from enum import Enum


class CollectionErrorType(str, Enum):
    COMMAND_FAILED = "command_failed"
    COMMAND_TIMEOUT = "command_timeout"
    PARSE_FAILED = "parse_failed"
    QGA_FAILED = "qga_failed"
    LIBVIRT_FAILED = "libvirt_failed"
    UNKNOWN = "unknown"

