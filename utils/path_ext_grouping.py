"""Group collected file paths by compound extension.

Artefact inventories contain ``.tar.gz``, ``.qcow2`` and ``.img`` files that
a naive ``os.path.splitext`` splits incorrectly.  Compound extension
grouping gives accurate counts for storage capacity planning.
"""

import logging
from typing import Dict, Iterable, List

LOG = logging.getLogger(__name__)

COMPOUND_SUFFIXES = (".tar.gz", ".tar.xz", ".tar.bz2", ".qcow2.part", ".img.part")


def extension_of(path: str) -> str:
    """Return the longest known extension for *path*."""
    lowered = path.lower()
    for suffix in COMPOUND_SUFFIXES:
        if lowered.endswith(suffix):
            return suffix
    base = path.rsplit("/", 1)[-1]
    if "." not in base:
        return ""
    return "." + base.rsplit(".", 1)[-1].lower()


def group_by_extension(paths: Iterable[str]) -> Dict[str, List[str]]:
    """Group paths by extension, using an empty key for extension-less ones."""
    groups: Dict[str, List[str]] = {}
    for path in paths:
        groups.setdefault(extension_of(path), []).append(path)
    LOG.debug("grouped %d path(s) into %d extension bucket(s)", len(list(paths)), len(groups))
    return groups


def top_extensions(paths: Iterable[str], limit: int = 5) -> List[str]:
    """Return the most frequent extensions in descending order."""
    groups = group_by_extension(paths)
    ordered = sorted(groups, key=lambda key: len(groups[key]), reverse=True)
    return ordered[: max(0, limit)]


__all__ = ["COMPOUND_SUFFIXES", "extension_of", "group_by_extension", "top_extensions"]
