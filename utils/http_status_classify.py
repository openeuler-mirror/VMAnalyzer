"""Classify HTTP status codes into their numeric class and semantics."""

_CLASSES = {1: "informational", 2: "success", 3: "redirect",
            4: "client_error", 5: "server_error"}


def status_class(code):
    """Return the descriptive class name for an HTTP status code."""
    return _CLASSES.get(int(code) // 100, "unknown")


def is_success(code):
    """Return True when the status code lies in the success class."""
    return 200 <= int(code) < 300


def is_redirect(code):
    """Return True when the status code indicates a redirect."""
    return 300 <= int(code) < 400


def is_retryable(code):
    """Return True for status codes generally safe to retry."""
    return int(code) in {408, 425, 429, 500, 502, 503, 504}


def describe_status(code):
    """Return a compact ``code class`` description string."""
    value = int(code)
    return "{} {}".format(value, status_class(value))


__all__ = ["status_class", "is_success", "is_redirect", "is_retryable", "describe_status"]
