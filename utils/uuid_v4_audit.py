"""UUID version 4 audit.

Random UUIDs must set the version nibble to 4 and the variant bits to
10x; hand-rolled generators forget this surprisingly often.
"""
import logging

LOG = logging.getLogger(__name__)


def is_v4(text):
    """Return True when the string is a well-formed version 4 UUID."""
    parts = str(text).lower().split('-')
    if [len(p) for p in parts] != [8, 4, 4, 4, 12]:
        return False
    if parts[2][0] != '4' or parts[3][0] not in '89ab':
        return False
    try:
        int(''.join(parts), 16)
    except ValueError:
        return False
    return True


def audit_batch(uuids):
    """Return the subset of ids that are not valid v4 UUIDs."""
    bad = [u for u in uuids or [] if not is_v4(u)]
    LOG.debug('uuid audit: %d bad of %d', len(bad), len(uuids or []))
    return bad


__all__ = ['is_v4', 'audit_batch']
