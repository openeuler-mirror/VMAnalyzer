#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Resolve VM identifiers across name, UUID and id forms."""

import logging

LOG = logging.getLogger(__name__)


def build_index(domains):
    """Index domains by every identifier they expose."""
    index = {}
    for domain in domains:
        for key in ("name", "uuid", "id"):
            value = domain.get(key)
            if value is None:
                continue
            index[str(value)] = domain
            index[str(value).lower()] = domain
    LOG.debug("indexed %d identifiers", len(index))
    return index


def resolve(index, identifier):
    """Look up a domain by any accepted identifier form."""
    if identifier is None:
        return None
    return index.get(str(identifier)) or index.get(str(identifier).lower())


def canonical_name(domain):
    """Return a stable display name for a domain record."""
    if not domain:
        return ""
    return str(domain.get("name") or domain.get("uuid") or domain.get("id") or "")
