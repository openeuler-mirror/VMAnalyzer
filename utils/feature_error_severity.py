"""Error severity mapper."""

from __future__ import annotations

SEVERITY_BY_TYPE = {
    "command_timeout": "warning",
    "parse_failed": "warning",
    "qga_failed": "critical",
    "libvirt_failed": "critical",
    "command_failed": "warning",
    "unknown": "info",
}


def severity_for(error_type: str) -> str:
    return SEVERITY_BY_TYPE.get(error_type, "info")

