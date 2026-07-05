"""Collection error schema."""

from __future__ import annotations

REQUIRED_ERROR_FIELDS = ("timestamp", "type", "message", "context")


def validate_error_payload(payload: dict) -> tuple[bool, list[str]]:
    missing = [field for field in REQUIRED_ERROR_FIELDS if field not in payload]
    return not missing, missing

