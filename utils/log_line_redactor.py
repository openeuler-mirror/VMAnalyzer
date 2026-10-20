"""Redact sensitive tokens from log lines while keeping structure readable."""

import re

LONG_TOKEN = 20
_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_IPV4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
_AUTH = re.compile(r"(?i)(authorization|password|token|secret|api[-_]?key)\s*[:=]\s*(\S+)")


def redact_emails(text):
    """Replace every email address with a stable placeholder."""
    return _EMAIL.sub("<email>", text or "")


def redact_secrets(text):
    """Mask the values of authentication style key/value pairs."""
    return _AUTH.sub(lambda m: "{}=<redacted>".format(m.group(1)), text or "")


def redact_ips(text, keep=False):
    """Replace IPv4 addresses with a placeholder unless ``keep`` is True."""
    return text if keep else _IPV4.sub("<ip>", text or "")


def redact_line(text):
    """Apply the standard redaction pipeline to a single log line."""
    return redact_ips(redact_secrets(redact_emails(text)))


__all__ = ["redact_emails", "redact_secrets", "redact_ips", "redact_line"]
