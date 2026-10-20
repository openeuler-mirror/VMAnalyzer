"""Parse ``/etc/mtab`` style mount lines into structured field dictionaries."""

_ESCAPES = {"\\040": " ", "\\011": "\t", "\\012": "\n", "\\134": "\\"}


def _unescape(text):
    """Decode the octal escapes used in mount tables."""
    for escaped, literal in _ESCAPES.items():
        text = text.replace(escaped, literal)
    return text


def parse_mount_line(line):
    """Return a dict of mount fields, or ``None`` for blank/malformed lines."""
    parts = (line or "").split()
    if len(parts) < 4:
        return None
    device, mountpoint, fstype, options = parts[0], parts[1], parts[2], parts[3]
    return {
        "device": _unescape(device),
        "mountpoint": _unescape(mountpoint),
        "fstype": fstype,
        "options": options.split(","),
        "dump": parts[4] if len(parts) > 4 else "0",
        "pass": parts[5] if len(parts) > 5 else "0",
    }


def find_mount(entries, mountpoint):
    """Return the parsed entry whose mountpoint matches, or ``None``."""
    for line in entries:
        parsed = parse_mount_line(line)
        if parsed and parsed["mountpoint"] == mountpoint:
            return parsed
    return None


def mounted_filesystems(entries):
    """Return the sorted list of mountpoints across all valid entries."""
    return sorted(parsed["mountpoint"] for parsed in map(parse_mount_line, entries) if parsed)


__all__ = ["parse_mount_line", "find_mount", "mounted_filesystems"]
