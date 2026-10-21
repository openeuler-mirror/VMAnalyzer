"""Identify common artefact types from their leading magic bytes.

Collectors sometimes record a size but not a type for dumped guest files.
Sniffing a few header bytes is enough to distinguish disk images, archives
and compressed traces without adding a libmagic dependency.
"""

import logging
from typing import Optional, Tuple

LOG = logging.getLogger(__name__)

MAGIC_TABLE: Tuple[Tuple[bytes, str], ...] = (
    (b"QFI\xfb", "qcow2"),
    (b"\x1f\x8b", "gzip"),
    (b"\xfd7zXZ\x00", "xz"),
    (b"BZh", "bzip2"),
    (b"(\xb5/\xfd", "zstd"),
    (b"\x7fELF", "elf"),
    (b"PK\x03\x04", "zip"),
)


def sniff_bytes(header: bytes) -> str:
    """Return a short artefact type for *header*, or ``unknown``."""
    for signature, label in MAGIC_TABLE:
        if header.startswith(signature):
            return label
    return "unknown"


def sniff_file(path: str, length: int = 8) -> str:
    """Read the first *length* bytes of *path* and identify its type."""
    try:
        with open(path, "rb") as handle:
            header = handle.read(length)
    except OSError as error:
        LOG.warning("cannot read header of %s: %s", path, error)
        return "unreadable"
    label = sniff_bytes(header)
    LOG.debug("sniffed %s as %s", path, label)
    return label


def is_compressed(path: str) -> Optional[bool]:
    """Return whether the file is compressed, or None when unreadable."""
    label = sniff_file(path)
    if label == "unreadable":
        return None
    return label in {"gzip", "xz", "bzip2", "zstd"}


__all__ = ["MAGIC_TABLE", "sniff_bytes", "sniff_file", "is_compressed"]
