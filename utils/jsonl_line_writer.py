"""Serialise records as newline-delimited JSON with size guarding.

JSONL consumers require exactly one object per line, which naive
``json.dumps`` output violates when values contain literal newlines.  The
writer escapes them and enforces a per-record size cap before emission.
"""

import json
import logging
from typing import Any, Dict, Iterable, List, Optional

LOG = logging.getLogger(__name__)


def encode_record(record: Dict[str, Any], max_bytes: Optional[int] = None) -> Optional[str]:
    """Return a single-line JSON encoding, or None when oversized."""
    line = json.dumps(record, ensure_ascii=False, separators=(",", ":"), default=str)
    line = line.replace("\r", "\\r").replace("\n", "\\n")
    if max_bytes is not None and len(line.encode("utf-8")) > max_bytes:
        LOG.warning("record dropped, %d bytes exceed the limit of %d",
                    len(line.encode("utf-8")), max_bytes)
        return None
    return line


def encode_records(records: Iterable[Dict[str, Any]],
                   max_bytes: Optional[int] = None) -> List[str]:
    """Encode a batch and silently skip records that are too large."""
    lines = [encode_record(record, max_bytes) for record in records]
    kept = [line for line in lines if line is not None]
    LOG.debug("encoded %d of %d record(s)", len(kept), len(lines))
    return kept


def decode_lines(text: str) -> List[Dict[str, Any]]:
    """Parse JSONL text, skipping blank and malformed lines."""
    records: List[Dict[str, Any]] = []
    for number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as error:
            LOG.warning("skipping malformed JSONL line %d: %s", number, error)
    return records


__all__ = ["encode_record", "encode_records", "decode_lines"]
