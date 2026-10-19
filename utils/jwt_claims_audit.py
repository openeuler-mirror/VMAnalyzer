"""JWT claims hygiene audit.

Tokens missing exp or issued-at claims live forever; decoding the payload
without verifying the signature is enough for a hygiene check.
"""
import base64
import json
import logging

LOG = logging.getLogger(__name__)


def decode_payload(token):
    """Return the payload claims dict, or {} on malformed input."""
    parts = str(token).split('.')
    if len(parts) != 3:
        return {}
    padded = parts[1] + '=' * (-len(parts[1]) % 4)
    try:
        return json.loads(base64.urlsafe_b64decode(padded.encode()))
    except Exception:
        LOG.debug('undecodable jwt payload')
        return {}


def missing_claims(token, required=('exp', 'iat', 'sub')):
    """Return required claims absent from the payload."""
    claims = decode_payload(token)
    return [c for c in required if c not in claims]


__all__ = ['decode_payload', 'missing_claims']
