"""Collection error classifier."""

from __future__ import annotations

def classify_error(message: str) -> str:
    text = (message or "").lower()
    if "timeout" in text or "timed out" in text:
        return "command_timeout"
    if "json" in text or "parse" in text or "decode" in text:
        return "parse_failed"
    if "qga" in text or "guest" in text:
        return "qga_failed"
    if "libvirt" in text or "virsh" in text:
        return "libvirt_failed"
    if "failed" in text or "exit code" in text:
        return "command_failed"
    return "unknown"

