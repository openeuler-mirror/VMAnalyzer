"""Build stable fingerprints for retryable request payloads.

Retry logic needs to detect that a repeated request is the same logical
operation.  Hashing a canonicalised subset of fields produces an identifier
that is stable across dict ordering and irrelevant whitespace.
"""

import hashlib
import json
import logging
from typing import Iterable, Optional

LOG = logging.getLogger(__name__)


def canonical_json(payload: dict, fields: Optional[Iterable[str]] = None) -> str:
    """Serialise a payload with sorted keys and compact separators."""
    if fields is not None:
        selected = {name: payload[name] for name in fields if name in payload}
    else:
        selected = payload
    return json.dumps(selected, sort_keys=True, separators=(",", ":"), default=str)


def fingerprint(payload: dict, fields: Optional[Iterable[str]] = None,
                length: int = 16) -> str:
    """Return a truncated SHA-256 fingerprint of the canonical payload."""
    digest = hashlib.sha256(canonical_json(payload, fields).encode("utf-8")).hexdigest()
    LOG.debug("fingerprint length %d", length)
    return digest[: max(1, min(int(length), 64))]


def is_repeat(previous: str, payload: dict, length: int = 16) -> bool:
    """Check whether *payload* matches a previously computed fingerprint."""
    return previous == fingerprint(payload, length=length)


__all__ = ["canonical_json", "fingerprint", "is_repeat"]
