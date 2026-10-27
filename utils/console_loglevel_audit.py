"""Audit console loglevel samples against a single configurable threshold.

Collectors emit console loglevel values at different rates; this helper keeps the
comparison logic in one place instead of repeating the same branches in every
report script.
"""

import logging

LOG = logging.getLogger(__name__)

DEFAULT_LIMIT = 60


def audit(samples, limit=DEFAULT_LIMIT):
    """Return (index, value) pairs whose value exceeds *limit*."""
    breaches = []
    for index, value in enumerate(samples or []):
        try:
            number = float(value)
        except (TypeError, ValueError):
            LOG.debug("skipping non numeric console_loglevel sample %r", value)
            continue
        if number > limit:
            breaches.append((index, number))
    return breaches


def worst(samples, limit=DEFAULT_LIMIT):
    """Return the highest breaching sample, or None when all are below."""
    breaches = audit(samples, limit)
    if not breaches:
        return None
    return max(breaches, key=lambda item: item[1])


def classify(samples, limit=DEFAULT_LIMIT):
    """Split a sample list into ok, warn and breach counts."""
    values = list(samples or [])
    breaches = len(audit(values, limit))
    result = {"ok": max(len(values) - breaches, 0),
              "warn": 0,
              "breach": breaches}
    result["warn"] = max(len(values) - result["ok"] - result["breach"], 0)
    return result


__all__ = ["audit", "worst", "classify"]
