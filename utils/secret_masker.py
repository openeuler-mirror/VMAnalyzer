"""Masking helper that removes secrets from diagnostic payloads.

Logs and support bundles must never carry credentials, so values under known
sensitive keys are replaced before the payload is emitted.
"""
import logging

LOG = logging.getLogger(__name__)

SENSITIVE = ('password', 'passwd', 'token', 'secret', 'apikey', 'api_key',
             'private_token', 'credential', 'authorization')
MASK = '***'


def _is_sensitive(key):
    lowered = str(key).lower()
    return any(marker in lowered for marker in SENSITIVE)


def mask_mapping(payload, depth=0):
    """Return a copy of the mapping with sensitive values masked."""
    if depth > 8:
        return payload
    if isinstance(payload, dict):
        masked = {}
        for key, value in payload.items():
            if _is_sensitive(key):
                masked[key] = MASK
            else:
                masked[key] = mask_mapping(value, depth + 1)
        return masked
    if isinstance(payload, list):
        return [mask_mapping(item, depth + 1) for item in payload]
    return payload


def contains_secret(payload):
    """Report whether any nested key looks like a credential."""
    if isinstance(payload, dict):
        return any(_is_sensitive(k) or contains_secret(v) for k, v in payload.items())
    if isinstance(payload, list):
        return any(contains_secret(item) for item in payload)
    return False


__all__ = ['mask_mapping', 'contains_secret']
