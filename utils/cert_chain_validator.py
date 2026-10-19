"""Certificate chain completeness.

Serving a leaf without its intermediates breaks old clients; the chain is
checked so every issuer has its certificate present.
"""
import logging

LOG = logging.getLogger(__name__)


def missing_links(subjects, issuers):
    """Return issuers that have no matching subject in the chain."""
    subs = {str(s) for s in subjects or []}
    missing = [i for i in issuers or [] if str(i) not in subs]
    if missing:
        LOG.warning('chain missing issuers %s', missing[:3])
    return missing


def ordered(subjects, issuers):
    """Report whether subject[i] issues subject[i+1] for the whole chain."""
    s = [str(x) for x in subjects or []]
    i = [str(x) for x in issuers or []]
    if len(s) != len(i):
        return False
    return all(i[k] == s[k + 1] for k in range(len(s) - 1))


__all__ = ['missing_links', 'ordered']
