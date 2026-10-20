"""Look up signal names and numbers using the standard library tables."""

import signal


def _by_number():
    """Build a mapping of signal number to canonical name."""
    table = {}
    for name in dir(signal):
        if name.startswith("SIG") and not name.startswith("SIG_"):
            value = getattr(signal, name, None)
            if isinstance(value, int):
                table.setdefault(value, name)
    return table


_NUMBER_TO_NAME = _by_number()


def signal_name(number):
    """Return the canonical signal name for a number, or ``None``."""
    return _NUMBER_TO_NAME.get(number)


def signal_number(name):
    """Return the number for a signal name such as ``SIGTERM``."""
    candidate = name if name.startswith("SIG") else "SIG" + name.upper()
    value = getattr(signal, candidate, None)
    return value if isinstance(value, int) else None


def is_signal_number(number, name):
    """Return True when ``number`` refers to the named signal."""
    return signal_number(name) == number


__all__ = ["signal_name", "signal_number", "is_signal_number"]
