"""Split a single CSV record honouring quoted fields."""
import logging

__all__ = ["split_csv_line", "join_csv_line"]

LOG = logging.getLogger(__name__)


def split_csv_line(line, delimiter=","):
    """Split *line* on *delimiter* while preserving quoted delimiters."""
    fields, buf, quoted, i = [], [], False, 0
    text = str(line).rstrip("\r\n")
    while i < len(text):
        ch = text[i]
        if ch == '"':
            if quoted and i + 1 < len(text) and text[i + 1] == '"':
                buf.append('"')
                i += 2
                continue
            quoted = not quoted
        elif ch == delimiter and not quoted:
            fields.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
        i += 1
    if quoted:
        LOG.debug("unterminated quoted field in CSV line")
    fields.append("".join(buf))
    return fields


def join_csv_line(fields, delimiter=","):
    """Quote and join *fields* back into a single CSV record."""
    out = []
    for field in fields:
        text = str(field)
        if any(c in text for c in (delimiter, '"', "\n")):
            out.append('"' + text.replace('"', '""') + '"')
        else:
            out.append(text)
    return delimiter.join(out)
