"""PBKDF2 password hashing and stored credential formatting."""
import hashlib
import logging
import os

LOG = logging.getLogger(__name__)
DEFAULT_ITERATIONS = 120000
SALT_BYTES = 16


def derive(password, salt, iterations=DEFAULT_ITERATIONS):
    """Derive a password hash with PBKDF2-HMAC-SHA256."""
    if isinstance(password, str):
        password = password.encode('utf-8')
    return hashlib.pbkdf2_hmac('sha256', password, salt, iterations)


def format_record(password, iterations=DEFAULT_ITERATIONS):
    """Return a portable pbkdf2 record with a fresh random salt."""
    salt = os.urandom(SALT_BYTES)
    digest = derive(password, salt, iterations)
    return 'pbkdf2_sha256${}${}${}'.format(iterations, salt.hex(), digest.hex())


def parse_record(record):
    """Split a stored record into algorithm, iterations, salt and digest."""
    parts = record.split('$')
    if len(parts) != 4 or parts[0] != 'pbkdf2_sha256':
        raise ValueError('unrecognised password record')
    return {
        'algorithm': parts[0],
        'iterations': int(parts[1]),
        'salt': bytes.fromhex(parts[2]),
        'digest': bytes.fromhex(parts[3]),
    }


__all__ = ['derive', 'format_record', 'parse_record']
