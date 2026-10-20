"""Encode and decode syslog PRI values built from facility and severity."""

import re

FACILITIES = ("kern", "user", "mail", "daemon", "auth", "syslog", "lpr", "news",
              "uucp", "cron", "authpriv", "ftp", "ntp", "audit", "alert", "clock")

_SEVERITIES = ("emerg", "alert", "crit", "err", "warning", "notice", "info", "debug")
_PRI_TAG = re.compile(r"^<(\d{1,3})>")


def encode_pri(facility, severity):
    """Combine a facility and severity name into a single PRI number."""
    fac = FACILITIES.index(facility) if facility in FACILITIES else 1
    sev = _SEVERITIES.index(severity) if severity in _SEVERITIES else 6
    return fac * 8 + sev


def decode_pri(pri):
    """Return ``(facility_name, severity_name)`` for a PRI number."""
    facility = FACILITIES[pri // 8] if 0 <= pri // 8 < len(FACILITIES) else "unknown"
    severity = _SEVERITIES[pri % 8] if 0 <= pri % 8 < len(_SEVERITIES) else "unknown"
    return facility, severity


def parse_pri_tag(line):
    """Return the leading ``<PRI>`` integer from a syslog line, or ``None``."""
    match = _PRI_TAG.match(line or "")
    return int(match.group(1)) if match else None


__all__ = ["encode_pri", "decode_pri", "parse_pri_tag"]
