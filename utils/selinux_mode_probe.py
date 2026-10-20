"""SELinux mode consistency.

Hosts drift from enforcing to permissive after debugging; the mode string is
normalised and compared to policy.
"""
import logging

LOG = logging.getLogger(__name__)


def normalise(mode):
    """Return the canonical lowercase SELinux mode."""
    m = str(mode or '').strip().lower()
    return m if m in ('enforcing', 'permissive', 'disabled') else 'unknown'


def compliant(mode, required='enforcing'):
    """Report whether the mode matches the required policy."""
    ok = normalise(mode) == required
    if not ok:
        LOG.warning('selinux mode %s != %s', mode, required)
    return ok


__all__ = ['normalise', 'compliant']
