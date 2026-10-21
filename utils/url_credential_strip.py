"""Remove embedded credentials from URLs before logging them.

Connection strings occasionally contain ``user:password@`` in the authority
section.  Logging such a URL leaks secrets, so the helper rewrites it while
keeping the URL otherwise parseable.
"""

import logging
import re

LOG = logging.getLogger(__name__)

CREDENTIAL_PATTERN = re.compile(r"(?P<scheme>[A-Za-z][\w+.-]*://)(?P<user>[^/@:]+):(?P<secret>[^/@]*)@")


def strip_credentials(url: str) -> str:
    """Return the URL with user information removed."""
    cleaned = CREDENTIAL_PATTERN.sub(lambda match: match.group("scheme"), url)
    if cleaned != url:
        LOG.debug("removed embedded credentials from URL")
    return cleaned


def contains_credentials(url: str) -> bool:
    """Return True when the URL embeds user information."""
    return bool(CREDENTIAL_PATTERN.search(url))


def redact_user(url: str) -> str:
    """Keep the user name but hide the password portion."""
    def replace(match):
        return "{}{}:****@".format(match.group("scheme"), match.group("user"))

    return CREDENTIAL_PATTERN.sub(replace, url)


__all__ = ["CREDENTIAL_PATTERN", "strip_credentials", "contains_credentials", "redact_user"]
