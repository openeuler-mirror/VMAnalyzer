"""Rank alert severity labels and pick the most severe among a set."""

import logging

_LEVELS = {"info": 10, "notice": 15, "low": 20, "warning": 30, "warn": 30,
           "minor": 35, "error": 40, "high": 50, "critical": 60, "fatal": 70,
           "emergency": 80}

_LEVEL = logging.getLogger(__name__)


def severity_rank(label):
    """Return a numeric rank for a severity label, defaulting to info."""
    return _LEVELS.get((label or "").strip().lower(), _LEVELS["info"])


def highest_severity(labels):
    """Return the label with the greatest rank from an iterable of labels."""
    best = None
    best_rank = -1
    for label in labels:
        rank = severity_rank(label)
        if rank > best_rank:
            best, best_rank = label, rank
    return best


def is_at_least(label, threshold):
    """Return True when ``label`` ranks at or above ``threshold``."""
    return severity_rank(label) >= severity_rank(threshold)


def merge_severities(*labels):
    """Return the most severe label out of the supplied arguments."""
    return highest_severity([label for label in labels if label]) or "info"


__all__ = ["severity_rank", "highest_severity", "is_at_least", "merge_severities"]
