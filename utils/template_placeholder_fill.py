"""Fill ``{name}`` placeholders in a template from a mapping."""
import logging
import re

__all__ = ["fill_template", "find_placeholders"]

LOG = logging.getLogger(__name__)
_PLACEHOLDER = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")


def find_placeholders(template):
    """Return the sorted unique placeholder names inside *template*."""
    return sorted(set(_PLACEHOLDER.findall(str(template))))


def fill_template(template, values, keep_unknown=True):
    """Substitute ``{name}`` occurrences using *values*."""

    def replace(match):
        key = match.group(1)
        if key in values:
            return str(values[key])
        LOG.debug("unknown placeholder %r left untouched", key)
        return match.group(0) if keep_unknown else ""

    return _PLACEHOLDER.sub(replace, str(template))
