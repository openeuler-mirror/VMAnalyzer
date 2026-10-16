"""Audit of file mode bits for overly permissive access.

World writable or group writable paths on a host monitored by the agent are a
standing risk, so their modes are flagged for review.
"""
import logging

LOG = logging.getLogger(__name__)


def parse_mode(text):
    """Parse an octal mode string such as '0644' into an integer."""
    cleaned = str(text).strip().lstrip('0o')
    if not cleaned:
        return 0
    try:
        return int(cleaned, 8)
    except ValueError:
        return 0


def is_world_writable(mode):
    """Report whether the other bits grant write access."""
    return bool(int(mode) & 0o002)


def is_group_writable(mode):
    """Report whether the group bits grant write access."""
    return bool(int(mode) & 0o020)


def audit_entries(entries, allow_group=False):
    """Return a list of (path, mode) that breach the writable policy."""
    breaches = []
    for path, mode in entries or []:
        bits = parse_mode(mode) if isinstance(mode, str) else int(mode)
        risky = is_world_writable(bits) or (is_group_writable(bits) and not allow_group)
        if risky:
            breaches.append((path, oct(bits)))
    if breaches:
        LOG.debug('%d paths violate the mode policy', len(breaches))
    return breaches


__all__ = ['parse_mode', 'is_world_writable', 'is_group_writable', 'audit_entries']
