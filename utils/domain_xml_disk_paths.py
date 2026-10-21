"""Extract disk source paths and targets from libvirt domain XML.

Disk paths are needed for capacity checks and for verifying that backing
files still exist.  A focused parser returns only the attributes that
matter instead of building the whole domain model.
"""

import logging
import re
from typing import List

LOG = logging.getLogger(__name__)

DISK_PATTERN = re.compile(r"<disk(?P<body>.*?)</disk>", re.DOTALL)
TARGET_PATTERN = re.compile(r"<target[^>]*dev\s*=\s*[\"']([^\"']+)[\"']")
SOURCE_PATTERN = re.compile(r"<source[^>]*file\s*=\s*[\"']([^\"']+)[\"']")
DEVICE_PATTERN = re.compile(r"device\s*=\s*[\"']([^\"']+)[\"']")


def disk_entries(xml_text: str) -> List[dict]:
    """Return one mapping per disk with target, source and device type."""
    entries: List[dict] = []
    for match in DISK_PATTERN.finditer(xml_text):
        body = match.group("body")
        target = TARGET_PATTERN.search(body)
        source = SOURCE_PATTERN.search(body)
        device = DEVICE_PATTERN.search(body)
        entries.append({
            "target": target.group(1) if target else "",
            "source": source.group(1) if source else "",
            "device": device.group(1) if device else "disk",
        })
    LOG.debug("extracted %d disk entry(ies)", len(entries))
    return entries


def source_paths(xml_text: str) -> List[str]:
    """Return only the non-empty source file paths."""
    return [entry["source"] for entry in disk_entries(xml_text) if entry["source"]]


def duplicate_targets(xml_text: str) -> List[str]:
    """Return disk targets that appear more than once."""
    seen, duplicates = set(), []
    for entry in disk_entries(xml_text):
        target = entry["target"]
        if target in seen and target not in duplicates:
            duplicates.append(target)
        seen.add(target)
    if duplicates:
        LOG.warning("duplicate disk target(s): %s", ", ".join(duplicates))
    return duplicates


__all__ = ["disk_entries", "source_paths", "duplicate_targets"]
