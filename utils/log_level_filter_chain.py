"""Evaluate an ordered chain of log level rules for a logger name.

Operators want to raise verbosity for one subsystem without changing the
global level.  Rules evaluated in order with the first match winning give
that control while keeping configuration readable.
"""

import logging
from typing import Iterable, List, Tuple

LOG = logging.getLogger(__name__)

LEVELS = {"debug": logging.DEBUG, "info": logging.INFO,
          "warning": logging.WARNING, "error": logging.ERROR, "critical": logging.CRITICAL}


def parse_rule(rule: str) -> Tuple[str, str]:
    """Parse ``prefix:level`` into its two components."""
    prefix, _, level = rule.partition(":")
    name = level.strip().lower()
    if name not in LEVELS:
        raise ValueError("unknown log level in rule {!r}".format(rule))
    return prefix.strip(), name


def resolve_level(logger_name: str, rules: Iterable[str],
                  default: str = "info") -> str:
    """Return the first rule level whose prefix matches the logger name."""
    for rule in rules:
        prefix, level = parse_rule(rule)
        if prefix == "*" or logger_name.startswith(prefix):
            LOG.debug("logger %s matched rule %r", logger_name, rule)
            return level
    return default.lower()


def build_levels(rules: Iterable[str], logger_names: List[str]) -> dict:
    """Resolve effective levels for a batch of logger names."""
    materialised: List[str] = list(rules)
    levels = {name: LEVELS[resolve_level(name, materialised)] for name in logger_names}
    LOG.debug("resolved levels for %d logger(s)", len(levels))
    return levels


__all__ = ["LEVELS", "parse_rule", "resolve_level", "build_levels"]
