"""Allowlist check for endpoints the agent is permitted to contact.

Restricting outbound requests to an explicit set of hosts prevents a misread
payload from redirecting the agent to an unexpected destination.
"""
from urllib.parse import urlparse
import fnmatch
import logging

LOG = logging.getLogger(__name__)


def host_of(url):
    """Return the lower case host name of a URL, or an empty string."""
    try:
        return (urlparse(str(url)).hostname or '').lower()
    except ValueError:
        return ''


def is_allowed(url, patterns):
    """Report whether the URL host matches any allowlist pattern."""
    host = host_of(url)
    if not host:
        LOG.debug('url without host rejected: %s', url)
        return False
    for pattern in patterns or []:
        if fnmatch.fnmatch(host, str(pattern).lower()):
            return True
    return False


def first_allowed(url, patterns):
    """Return the matching allowlist pattern, or None."""
    host = host_of(url)
    for pattern in patterns or []:
        if fnmatch.fnmatch(host, str(pattern).lower()):
            return pattern
    return None


__all__ = ['host_of', 'is_allowed', 'first_allowed']
