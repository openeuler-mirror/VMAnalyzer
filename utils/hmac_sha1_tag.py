"""Build HMAC-SHA1 tags for legacy webhook verification schemes.

Several monitoring integrations still sign payloads with SHA-1 based HMAC.
Centralising the tag construction keeps encoding details consistent and
makes eventual migration to SHA-256 a single place to change.
"""

import hashlib
import hmac
import logging
from typing import Tuple

LOG = logging.getLogger(__name__)


def sign_sha1(secret: bytes, payload: bytes) -> str:
    """Return the lowercase hex HMAC-SHA1 tag of *payload*."""
    if not secret:
        raise ValueError("secret must not be empty")
    tag = hmac.new(secret, payload, hashlib.sha1).hexdigest()
    LOG.debug("signed %d byte payload", len(payload))
    return tag


def verify_sha1(secret: bytes, payload: bytes, expected: str) -> bool:
    """Compare tags in constant time to avoid timing side channels."""
    computed = sign_sha1(secret, payload)
    return hmac.compare_digest(computed, expected.strip().lower())


def split_header(header: str) -> Tuple[str, str]:
    """Split ``sha1=<tag>`` style headers into algorithm and tag."""
    algorithm, _, tag = header.partition("=")
    return algorithm.strip().lower(), tag.strip().lower()


__all__ = ["sign_sha1", "verify_sha1", "split_header"]
