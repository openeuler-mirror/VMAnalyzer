"""Convert memory sizes into page counts for a given page size.

Hugepage sizing and balloon calculations need page counts, but operators
specify megabytes.  Handling non-divisible sizes explicitly avoids silently
under-allocating memory.
"""

import logging
from typing import Dict

LOG = logging.getLogger(__name__)

DEFAULT_PAGE_KB = 4


def megabytes_to_pages(megabytes: float, page_kb: int = DEFAULT_PAGE_KB) -> float:
    """Return the exact page count, allowing fractional pages."""
    if page_kb <= 0:
        raise ValueError("page_kb must be positive")
    return float(megabytes) * 1024.0 / page_kb


def whole_pages(megabytes: float, page_kb: int = DEFAULT_PAGE_KB) -> int:
    """Return the number of complete pages that fit."""
    return int(megabytes_to_pages(megabytes, page_kb))


def describe(megabytes: float, page_kb: int = DEFAULT_PAGE_KB) -> Dict[str, float]:
    """Return page counts plus the memory lost to rounding."""
    pages = megabytes_to_pages(megabytes, page_kb)
    whole = int(pages)
    wasted_kb = round((pages - whole) * page_kb, 3)
    result = {"pages": pages, "whole_pages": whole, "wasted_kb": wasted_kb}
    if wasted_kb > 0:
        LOG.debug("rounding wastes %.2f KB of memory", wasted_kb)
    return result


__all__ = ["DEFAULT_PAGE_KB", "megabytes_to_pages", "whole_pages", "describe"]
