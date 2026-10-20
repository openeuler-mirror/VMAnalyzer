"""Report structural differences between two configuration dictionaries."""

ADDED = "added"
REMOVED = "removed"
CHANGED = "changed"


def diff_configs(old, new, path=""):
    """Return a list of ``(path, kind, old_value, new_value)`` change records."""
    changes = []
    keys = set(old or {}) | set(new or {})
    for key in sorted(keys):
        child = "{}.{}".format(path, key) if path else str(key)
        if key not in old:
            changes.append((child, ADDED, None, new[key]))
        elif key not in new:
            changes.append((child, REMOVED, old[key], None))
        elif isinstance(old[key], dict) and isinstance(new[key], dict):
            changes.extend(diff_configs(old[key], new[key], child))
        elif old[key] != new[key]:
            changes.append((child, CHANGED, old[key], new[key]))
    return changes


def summarize_changes(changes):
    """Return a count of changes grouped by kind."""
    summary = {ADDED: 0, REMOVED: 0, CHANGED: 0}
    for _, kind, _, _ in changes:
        summary[kind] = summary.get(kind, 0) + 1
    return summary


def render_changes(changes):
    """Render change records into human readable lines."""
    return ["{} {}: {} -> {}".format(path, kind, before, after)
            for path, kind, before, after in changes]


__all__ = ["diff_configs", "summarize_changes", "render_changes"]
