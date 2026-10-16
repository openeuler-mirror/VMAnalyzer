"""Environment variable auditing for the agent runtime.

Configuration delivered through the environment is easy to mistype and hard to
trace, so these helpers locate missing variables and redact secrets before the
values reach any report.
"""
import os
import logging

LOG = logging.getLogger(__name__)

SECRET_HINTS = ('token', 'secret', 'password', 'key')


def missing_variables(names, environ=None):
    """Return required environment variables that are absent or empty."""
    env = environ if environ is not None else os.environ
    missing = [name for name in names or [] if not env.get(name)]
    if missing:
        LOG.info('missing environment variables: %s', ', '.join(missing))
    return missing


def is_secret_name(name):
    """Report whether a variable name looks like it carries a secret."""
    lowered = str(name).lower()
    return any(hint in lowered for hint in SECRET_HINTS)


def redact(name, value):
    """Mask a secret value, keeping only its length for diagnostics."""
    if not is_secret_name(name):
        return value
    return '<redacted:%d>' % len(str(value))


__all__ = ['missing_variables', 'is_secret_name', 'redact']
