"""Strip byte-order marks and zero-width prefixes from decoded text.

Configuration files copied between Windows and Linux hosts often carry a
UTF-8 BOM or an inherited zero-width space before the first key.  Removing
the marker keeps downstream parsers from treating the leading key as
unknown and from emitting misleading "missing key" diagnostics.
"""

import logging
from typing import Iterable, List, Optional

LOG = logging.getLogger(__name__)

BOM_MARKERS = ("\ufeff", "\u200b", "\u2060")


def strip_bom(text: str, markers: Optional[Iterable[str]] = None) -> str:
    """Remove leading BOM-like characters from *text*."""
    candidates = tuple(markers) if markers is not None else BOM_MARKERS
    trimmed = text
    while trimmed:
        for marker in candidates:
            if trimmed.startswith(marker):
                trimmed = trimmed[len(marker):]
                break
        else:
            break
    if trimmed != text:
        LOG.debug("stripped %d leading marker character(s)", len(text) - len(trimmed))
    return trimmed


def strip_bom_lines(lines: Iterable[str]) -> List[str]:
    """Strip markers from every line while preserving line endings."""
    return [strip_bom(line) for line in lines]


__all__ = ["BOM_MARKERS", "strip_bom", "strip_bom_lines"]
