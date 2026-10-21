"""Unwrap QEMU guest agent replies and decode base64 output fields.

The agent nests results under ``return`` and returns ``out-data`` as base64.
Centralising the unwrapping logic keeps every collector's decoding
consistent and makes error extraction straightforward.
"""

import base64
import binascii
import json
import logging
from typing import Optional, Tuple

LOG = logging.getLogger(__name__)


def unwrap(payload: str) -> Tuple[Optional[dict], Optional[str]]:
    """Return ``(result, error)`` extracted from an agent reply."""
    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError as error:
        return None, "invalid json: {}".format(error)
    if "error" in parsed:
        detail = parsed.get("error", {}).get("desc", "unknown agent error")
        return None, str(detail)
    result = parsed.get("return")
    if not isinstance(result, dict):
        return None, "missing return object"
    return result, None


def decode_output(result: dict, field: str = "out-data") -> str:
    """Decode a base64 output field, returning an empty string on failure."""
    encoded = result.get(field, "")
    if not encoded:
        return ""
    try:
        return base64.b64decode(encoded).decode("utf-8", errors="replace")
    except (binascii.Error, ValueError) as error:
        LOG.warning("cannot decode agent output field %s: %s", field, error)
        return ""


def exit_status(result: dict) -> Optional[int]:
    """Return the exit code reported by a completed guest command."""
    value = result.get("exitcode")
    return int(value) if isinstance(value, int) else None


__all__ = ["unwrap", "decode_output", "exit_status"]
