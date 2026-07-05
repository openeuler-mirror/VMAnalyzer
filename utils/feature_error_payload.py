"""Structured error payload helper."""

from __future__ import annotations

from datetime import datetime


def build_error_payload(error_type: str, message: str, context: dict | None = None) -> dict:
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "type": error_type,
        "message": message,
        "context": context or {},
    }

