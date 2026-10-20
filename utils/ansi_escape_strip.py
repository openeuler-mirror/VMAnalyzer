"""Remove ANSI SGR / CSI escape sequences from terminal text."""
import re

__all__ = ["strip_ansi", "has_ansi", "strip_ansi_lines", "find_ansi_codes"]

_ANSI = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]|\x1b\][^\x07]*\x07")


def strip_ansi(text):
    """Return *text* with all ANSI escape sequences removed."""
    return _ANSI.sub("", str(text))


def has_ansi(text):
    """Return True when *text* contains at least one ANSI sequence."""
    return bool(_ANSI.search(str(text)))


def strip_ansi_lines(lines):
    """Strip ANSI escapes from every line in *lines*."""
    return [strip_ansi(line) for line in lines]


def find_ansi_codes(text):
    """Return the list of ANSI sequences found in *text*."""
    return _ANSI.findall(str(text))
