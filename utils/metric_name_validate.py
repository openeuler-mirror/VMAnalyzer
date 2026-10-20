"""Validate Prometheus style metric names and label names as strings."""

import re

_METRIC = re.compile(r"^[a-zA-Z_:][a-zA-Z0-9_:]*$")
_LABEL = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
_RESERVED = ("__",)


def is_valid_metric_name(name):
    """Return True when the name follows the Prometheus metric grammar."""
    return bool(name) and bool(_METRIC.match(name))


def is_valid_label_name(name):
    """Return True when the name follows the Prometheus label grammar."""
    return bool(name) and bool(_LABEL.match(name))


def is_reserved(name):
    """Return True when a label name sits in the reserved ``__`` namespace."""
    return (name or "").startswith(_RESERVED)


def metric_name_issues(name):
    """Return a list of reasons a metric name would be rejected."""
    issues = []
    if not name:
        return ["name is empty"]
    if not is_valid_metric_name(name):
        issues.append("name contains invalid characters")
    if name.startswith("_"):
        issues.append("leading underscore is reserved")
    return issues


__all__ = ["is_valid_metric_name", "is_valid_label_name", "is_reserved", "metric_name_issues"]
