"""Match strings against simple ``*`` and ``?`` wildcard patterns."""
import re

__all__ = ["glob_match", "compile_glob", "any_glob_match", "filter_globs"]


def compile_glob(pattern, case_sensitive=True):
    """Compile a wildcard pattern into a regular expression object."""
    escaped = [re.escape(ch) if ch not in "*?" else "." + ch for ch in str(pattern)]
    flags = 0 if case_sensitive else re.IGNORECASE
    return re.compile("^" + "".join(escaped) + "$", flags)


def glob_match(pattern, text, case_sensitive=True):
    """Return True when *text* matches the wildcard *pattern*."""
    return bool(compile_glob(pattern, case_sensitive).match(str(text)))


def any_glob_match(patterns, text, case_sensitive=True):
    """Return True when *text* matches any pattern in *patterns*."""
    return any(glob_match(p, text, case_sensitive) for p in patterns)


def filter_globs(patterns, values, case_sensitive=True):
    """Return the *values* that match at least one of *patterns*."""
    return [v for v in values if any_glob_match(patterns, v, case_sensitive)]
