"""Validate Kubernetes object names against the DNS subdomain rules."""

import re

_DNS_SUBDOMAIN = re.compile(r"^[a-z0-9]([-a-z0-9]*[a-z0-9])?(\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*$")
_DNS_LABEL = re.compile(r"^[a-z0-9]([-a-z0-9]*[a-z0-9])?$")


def is_dns_subdomain(name, max_length=253):
    """Return True when a name obeys the DNS-1123 subdomain constraints."""
    return bool(name) and len(name) <= max_length and bool(_DNS_SUBDOMAIN.match(name))


def is_dns_label(name, max_length=63):
    """Return True when a name obeys the single DNS-1123 label constraints."""
    return bool(name) and len(name) <= max_length and bool(_DNS_LABEL.match(name))


def validation_errors(name):
    """Return a list of human readable reasons a name would be rejected."""
    errors = []
    if not name:
        return ["name is empty"]
    if len(name) > 253:
        errors.append("name exceeds 253 characters")
    if name.lower() != name:
        errors.append("name must be lowercase")
    if not is_dns_subdomain(name):
        errors.append("name is not a valid DNS subdomain")
    return errors


__all__ = ["is_dns_subdomain", "is_dns_label", "validation_errors"]
