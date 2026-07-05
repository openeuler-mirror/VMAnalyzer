"""Risk severity mapper."""

from __future__ import annotations

SEVERITY_BY_TAG = {
    "high_cpu": "warning",
    "high_memory": "warning",
    "high_disk": "critical",
    "network_drops": "warning",
    "collection_errors": "critical",
}


def severity_for_tag(tag: str) -> str:
    return SEVERITY_BY_TAG.get(tag, "info")

