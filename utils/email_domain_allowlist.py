"""Validate email addresses against a domain allow list.

Guest contact fields occasionally carry typos or external addresses that
must not receive alerts.  Checking the domain separately keeps the policy
readable and avoids rewriting regular expressions per deployment.
"""

import logging
from typing import Iterable, List, Optional

LOG = logging.getLogger(__name__)


def split_email(value: str) -> Optional[tuple]:
    """Return ``(local_part, domain)`` for a simple email, or None."""
    text = value.strip()
    if text.count("@") != 1:
        LOG.warning("rejecting malformed email %r", value)
        return None
    local, _, domain = text.partition("@")
    if not local or "." not in domain or domain.startswith(".") or domain.endswith("."):
        return None
    return local, domain.lower()


def is_allowed(value: str, domains: Iterable[str]) -> bool:
    """Return True when the email domain is inside the allow list."""
    parsed = split_email(value)
    if parsed is None:
        return False
    allowed = {domain.lower().lstrip("@") for domain in domains}
    matched = parsed[1] in allowed
    if not matched:
        LOG.info("email domain %s is not allow-listed", parsed[1])
    return matched


def filter_allowed(values: Iterable[str], domains: Iterable[str]) -> List[str]:
    """Return only the allow-listed addresses, preserving input order."""
    permitted = list(domains)
    kept = [value for value in values if is_allowed(value, permitted)]
    LOG.debug("kept %d of %d email address(es)", len(kept), len(list(values)))
    return kept


__all__ = ["split_email", "is_allowed", "filter_allowed"]
