"""Apply RFC 7396 JSON merge patch semantics."""
import copy
import logging

LOG = logging.getLogger(__name__)


def merge(target, patch):
    """Return a new document with a merge patch applied."""
    if not isinstance(patch, dict):
        return copy.deepcopy(patch)
    result = copy.deepcopy(target) if isinstance(target, dict) else {}
    for key, value in patch.items():
        if value is None:
            result.pop(key, None)
        else:
            result[key] = merge(result.get(key), value)
    return result


def apply_in_place(target, patch):
    """Mutate target by applying the merge patch."""
    if not isinstance(target, dict) or not isinstance(patch, dict):
        raise TypeError('both target and patch must be objects')
    for key, value in patch.items():
        if value is None:
            target.pop(key, None)
        elif isinstance(value, dict):
            child = target.get(key)
            if not isinstance(child, dict):
                child = {}
                target[key] = child
            apply_in_place(child, value)
        else:
            target[key] = copy.deepcopy(value)
    return target


__all__ = ['merge', 'apply_in_place']
