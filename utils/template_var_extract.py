"""Extract and report template variables in ``${name}`` style."""
import re

__all__ = ["extract_variables", "missing_variables"]

_VAR = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}|\$([A-Za-z_][A-Za-z0-9_]*)")


def extract_variables(template):
    """Return the ordered list of variable names referenced in *template*."""
    names = []
    for brace, bare in _VAR.findall(str(template)):
        name = brace or bare
        if name not in names:
            names.append(name)
    return names


def missing_variables(template, supplied):
    """Return variables referenced in *template* but absent from *supplied*."""
    known = set(supplied)
    return [name for name in extract_variables(template) if name not in known]
