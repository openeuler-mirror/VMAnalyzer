"""Match Kubernetes style label selectors against a label dictionary."""

_IN = "in"
_NOTIN = "notin"
_EXISTS = "exists"


def parse_selector(expression):
    """Parse a ``key=value``, ``key in (a,b)`` or ``key`` selector clause."""
    text = (expression or "").strip()
    if " notin " in text:
        key, values = text.split(" notin ", 1)
        return key.strip(), _NOTIN, [v.strip() for v in values.strip("() ").split(",")]
    if " in " in text:
        key, values = text.split(" in ", 1)
        return key.strip(), _IN, [v.strip() for v in values.strip("() ").split(",")]
    if "!=" in text:
        key, value = text.split("!=", 1)
        return key.strip(), _NOTIN, [value.strip()]
    if "=" in text:
        key, value = text.split("=", 1)
        return key.strip(), _IN, [value.strip()]
    return text, _EXISTS, []


def match_clause(labels, expression):
    """Return True when a single selector clause matches the labels."""
    key, operator, values = parse_selector(expression)
    if operator == _EXISTS:
        return key in labels
    if key not in labels:
        return operator == _NOTIN
    if operator == _IN:
        return labels[key] in values
    return labels[key] not in values


def match_selector(labels, selector):
    """Return True when every comma separated clause matches the labels."""
    clauses = [part for part in (selector or "").split(",") if part.strip()]
    return all(match_clause(labels, clause) for clause in clauses)


__all__ = ["parse_selector", "match_clause", "match_selector"]
