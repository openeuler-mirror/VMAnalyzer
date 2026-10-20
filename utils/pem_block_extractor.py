"""Extract PEM style ``BEGIN``/``END`` blocks from an in-memory text buffer."""

import re

_BLOCK = re.compile(
    r"-----BEGIN ([A-Z0-9 ]+)-----(.*?)-----END \1-----", re.DOTALL)


def extract_pem_blocks(text):
    """Return a list of ``(label, body)`` tuples for every PEM block found."""
    blocks = []
    for match in _BLOCK.finditer(text or ""):
        label = match.group(1).strip()
        body = "".join(match.group(2).split())
        blocks.append((label, body))
    return blocks


def pem_labels(text):
    """Return the sorted distinct labels of all PEM blocks in the text."""
    return sorted({label for label, _ in extract_pem_blocks(text)})


def has_certificate(text):
    """Return True when a CERTIFICATE PEM block is present."""
    return "CERTIFICATE" in pem_labels(text)


__all__ = ["extract_pem_blocks", "pem_labels", "has_certificate"]
