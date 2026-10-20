"""Remove line and block comments from source-like text."""
__all__ = ["strip_line_comments", "strip_block_comments", "strip_comments"]


def strip_line_comments(text, marker="#"):
    """Drop *marker* comments, keeping the code portion of each line."""
    out = []
    for line in str(text).splitlines():
        code, sep, _ = line.partition(marker)
        out.append(code.rstrip() if sep else line.rstrip())
    return "\n".join(out)


def strip_block_comments(text, start="/*", end="*/"):
    """Remove all *start* to *end* comment regions from *text*."""
    body = str(text)
    result, cursor, length = [], 0, len(body)
    while cursor < length:
        begin = body.find(start, cursor)
        if begin == -1:
            result.append(body[cursor:])
            break
        result.append(body[cursor:begin])
        finish = body.find(end, begin + len(start))
        cursor = length if finish == -1 else finish + len(end)
    return "".join(result)


def strip_comments(text, line_marker="//"):
    """Strip block then line comments using C-style markers."""
    return strip_line_comments(strip_block_comments(text), marker=line_marker)
