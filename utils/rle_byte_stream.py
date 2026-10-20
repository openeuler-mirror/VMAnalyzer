"""Compact run length encoding tailored to byte streams."""
import logging

LOG = logging.getLogger(__name__)
MAX_RUN = 255


def encode(data):
    """Encode a bytes-like object into (count, byte) run pairs."""
    encoded = bytearray()
    index = 0
    while index < len(data):
        byte = data[index]
        run = 1
        while index + run < len(data) and data[index + run] == byte and run < MAX_RUN:
            run += 1
        encoded.append(run)
        encoded.append(byte)
        index += run
    return bytes(encoded)


def decode(encoded):
    """Expand encoded run pairs back into the original byte stream."""
    if len(encoded) % 2:
        raise ValueError('encoded stream must contain whole run pairs')
    out = bytearray()
    for index in range(0, len(encoded), 2):
        out.extend([encoded[index + 1]] * encoded[index])
    return bytes(out)


def is_worthwhile(data, encoded):
    """Report whether encoding actually reduced the payload size."""
    return len(encoded) < len(data)


__all__ = ['encode', 'decode', 'is_worthwhile']
