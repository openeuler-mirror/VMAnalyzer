"""Index XML attributes by element tag for quick lookups.

Guest domain XML is large and frequently queried during collection.  A
lightweight regex-based index avoids building a full DOM when only a few
attributes are needed, which keeps per-collection overhead low.
"""

import logging
import re
from typing import Dict, List

LOG = logging.getLogger(__name__)

ELEMENT_PATTERN = re.compile(r"<(?P<tag>[A-Za-z_][\w.-]*)(?P<attrs>[^>]*?)/?>")
ATTRIBUTE_PATTERN = re.compile(r"(?P<name>[A-Za-z_][\w.:-]*)\s*=\s*[\"'](?P<value>[^\"']*)[\"']")


def index_attributes(xml_text: str) -> Dict[str, List[Dict[str, str]]]:
    """Map element tags to the attributes of every occurrence."""
    index: Dict[str, List[Dict[str, str]]] = {}
    for match in ELEMENT_PATTERN.finditer(xml_text):
        tag = match.group("tag")
        attributes = {item.group("name"): item.group("value")
                      for item in ATTRIBUTE_PATTERN.finditer(match.group("attrs"))}
        index.setdefault(tag, []).append(attributes)
    LOG.debug("indexed %d element tag(s)", len(index))
    return index


def first_attribute(index: Dict[str, List[Dict[str, str]]], tag: str,
                    name: str) -> str:
    """Return the first value of *name* on *tag*, or an empty string."""
    for attributes in index.get(tag, []):
        if name in attributes:
            return attributes[name]
    return ""


def attribute_values(index: Dict[str, List[Dict[str, str]]], tag: str,
                     name: str) -> List[str]:
    """Return every value of *name* across occurrences of *tag*."""
    return [attributes[name] for attributes in index.get(tag, []) if name in attributes]


__all__ = ["ELEMENT_PATTERN", "ATTRIBUTE_PATTERN", "index_attributes",
          "first_attribute", "attribute_values"]
