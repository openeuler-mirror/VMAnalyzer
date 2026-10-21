"""Classify a Linux process state character into a coarse category."""

_STATES = {"R": "running", "S": "sleeping", "D": "uninterruptible",
           "T": "stopped", "t": "tracing", "Z": "zombie", "X": "dead",
           "I": "idle", "W": "paging", "P": "parked"}

_ALIVE = {"running", "sleeping", "uninterruptible", "idle"}


def classify_state(letter):
    """Map a single state character to a descriptive category."""
    return _STATES.get((letter or "").strip()[:1], "unknown")


def is_alive(state_letter):
    """Return True when the process state counts as actively alive."""
    return classify_state(state_letter) in _ALIVE


def is_problem(state_letter):
    """Return True for states that usually warrant investigation."""
    return classify_state(state_letter) in {"zombie", "dead", "uninterruptible", "stopped"}


def describe_state_line(letter, comm=""):
    """Return a readable one line description for a process state."""
    return "{name}[{letter}] is {state}".format(
        name=comm or "process", letter=(letter or "?"), state=classify_state(letter))


__all__ = ["classify_state", "is_alive", "is_problem", "describe_state_line"]
