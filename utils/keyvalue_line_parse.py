"""Parse simple ``key=value`` log lines into dictionaries."""
import logging

__all__ = ["parse_kv_line", "parse_kv_lines"]

LOG = logging.getLogger(__name__)


def parse_kv_line(line, separator="=", comment="#"):
    """Return a dict of the key/value pairs found in one line."""
    result = {}
    text = str(line).strip()
    if not text or (comment and text.startswith(comment)):
        return result
    for chunk in text.split():
        if separator not in chunk:
            continue
        key, _, value = chunk.partition(separator)
        if key:
            result[key] = value.strip('"')
    return result


def parse_kv_lines(lines, separator="="):
    """Parse many lines, dropping the ones that yield no pairs."""
    parsed = (parse_kv_line(line, separator=separator) for line in lines)
    rows = [row for row in parsed if row]
    LOG.debug("parsed %d non-empty key/value rows", len(rows))
    return rows
