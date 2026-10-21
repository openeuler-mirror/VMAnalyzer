"""Attach consistent metadata tags to every collected record.

Reports from different hosts are indistinguishable without a source tag.
Injecting host, agent and collection identifiers at one place keeps every
downstream record self-describing.
"""

import logging

LOG = logging.getLogger(__name__)

RESERVED = ("host", "agent_version", "collected_at", "vm")


def build_tags(host, agent_version, collected_at):
    """Return the mandatory tag set for a collection round."""
    if not host:
        raise ValueError("host name is required for tagging")
    tags = {
        "host": str(host),
        "agent_version": str(agent_version),
        "collected_at": float(collected_at),
    }
    LOG.debug("built base tags for host %s", host)
    return tags


def apply_tags(record, tags, overwrite=False):
    """Return a copy of *record* with tags merged in."""
    merged = dict(record)
    added = 0
    for key, value in tags.items():
        if key in merged and not overwrite:
            continue
        if key not in merged:
            added += 1
        merged[key] = value
    LOG.debug("applied %d tag(s) to a record", added)
    return merged


def missing_tags(record):
    """Return reserved tags absent from a record."""
    return [name for name in RESERVED if name not in record]
