"""Evaluate feature-flag rules against a context mapping of attributes."""

import re

_OPERATORS = {"eq": lambda a, b: a == b,
              "ne": lambda a, b: a != b,
              "in": lambda a, b: a in b,
              "gte": lambda a, b: a >= b,
              "lte": lambda a, b: a <= b}


def _coerce(value):
    """Coerce numeric looking strings into ints for comparisons."""
    if isinstance(value, str) and re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def evaluate_rule(rule, context):
    """Return True when a single ``field/op/value`` rule matches the context."""
    field = rule.get("field")
    operator = rule.get("op", "eq")
    expected = _coerce(rule.get("value"))
    actual = _coerce(context.get(field))
    func = _OPERATORS.get(operator)
    if func is None:
        return False
    try:
        return bool(func(actual, expected))
    except TypeError:
        return False


def evaluate_flag(rules, context, match_all=True):
    """Evaluate a list of rules, requiring all or any to pass."""
    results = [evaluate_rule(rule, context) for rule in rules]
    return all(results) if match_all else any(results)


def flag_state(enabled, rules, context, match_all=True):
    """Return ``on`` or ``off`` combining the static flag and rule outcome."""
    return "on" if enabled and evaluate_flag(rules, context, match_all) else "off"


__all__ = ["evaluate_rule", "evaluate_flag", "flag_state"]
