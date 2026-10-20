"""Translate process exit codes into short diagnostic descriptions."""

_SIGNAL_BASE = 128

_COMMON = {
    0: "success",
    1: "general error",
    2: "misuse of shell builtin",
    126: "command not executable",
    127: "command not found",
    128: "invalid exit argument",
    130: "terminated by SIGINT",
    137: "killed by SIGKILL",
    143: "terminated by SIGTERM",
}


def describe_exit(code):
    """Return a description for an exit code, decoding signal offsets."""
    if code in _COMMON:
        return _COMMON[code]
    if code > _SIGNAL_BASE:
        return "terminated by signal {}".format(code - _SIGNAL_BASE)
    return "exit code {}".format(code)


def is_success(code):
    """Return True when the exit code denotes success."""
    return code == 0


def signal_from_exit(code):
    """Return the implied signal number, or ``None`` when not signal based."""
    if code >= _SIGNAL_BASE:
        return code - _SIGNAL_BASE
    return None


__all__ = ["describe_exit", "is_success", "signal_from_exit"]
