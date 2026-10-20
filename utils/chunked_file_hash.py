"""Hash files incrementally without loading them fully."""
import hashlib
import logging

LOG = logging.getLogger(__name__)
CHUNK_SIZE = 1 << 20


def hash_stream(stream, algorithm='sha256', chunk_size=CHUNK_SIZE):
    """Hash a binary stream by reading it in fixed size chunks."""
    digest = hashlib.new(algorithm)
    while True:
        chunk = stream.read(chunk_size)
        if not chunk:
            break
        digest.update(chunk)
    return digest.hexdigest()


def hash_path(path, algorithm='sha256', chunk_size=CHUNK_SIZE):
    """Hash a file on disk, reading it incrementally."""
    with open(path, 'rb') as handle:
        return hash_stream(handle, algorithm, chunk_size)


def verify_path(path, expected, algorithm='sha256'):
    """Report whether a file digest matches an expected hex value."""
    return hash_path(path, algorithm) == expected.strip().lower()


__all__ = ['hash_stream', 'hash_path', 'verify_path']
