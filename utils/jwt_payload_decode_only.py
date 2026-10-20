"""Decode the payload segment of a JWT for inspection; signature is never checked."""

import base64
import binascii
import json


def _b64url_decode(segment):
    """Decode a base64url segment, restoring padding as needed."""
    padded = segment + "=" * (-len(segment) % 4)
    return base64.urlsafe_b64decode(padded.encode("ascii"))


def decode_payload(token):
    """Return the decoded payload as a dict, or ``None`` when malformed."""
    parts = (token or "").split(".")
    if len(parts) < 2:
        return None
    try:
        payload = json.loads(_b64url_decode(parts[1]).decode("utf-8"))
    except (binascii.Error, ValueError, UnicodeDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def claim_names(token):
    """Return the sorted claim names present in the payload."""
    payload = decode_payload(token)
    return sorted(payload) if payload else []


def has_expiry(token):
    """Return True when the payload carries a numeric ``exp`` claim."""
    payload = decode_payload(token)
    return isinstance(payload, dict) and isinstance(payload.get("exp"), (int, float))


__all__ = ["decode_payload", "claim_names", "has_expiry"]
