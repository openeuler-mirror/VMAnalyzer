"""Normalise metric units before samples are stored.

Collectors label values with units such as ``KB``, ``kB`` or ``kib``.  A
canonical unit table prevents a fifty-fold discrepancy when one collector
means kilobytes and another means kibibytes.
"""

import logging

LOG = logging.getLogger(__name__)

UNIT_SCALE = {
    "b": 1.0, "byte": 1.0, "bytes": 1.0,
    "kb": 1000.0, "kib": 1024.0,
    "mb": 1000.0 ** 2, "mib": 1024.0 ** 2,
    "gb": 1000.0 ** 3, "gib": 1024.0 ** 3,
    "s": 1.0, "ms": 0.001, "us": 0.000001,
}


def canonical_unit(unit):
    """Return the lowercase canonical unit name."""
    key = str(unit).strip().lower()
    if key not in UNIT_SCALE:
        raise ValueError("unknown metric unit {!r}".format(unit))
    return key


def to_base(value, unit):
    """Convert a value into base units (bytes or seconds)."""
    key = canonical_unit(unit)
    return round(float(value) * UNIT_SCALE[key], 6)


def convert(value, source, target):
    """Convert a value between two compatible units."""
    base = to_base(value, source)
    divisor = UNIT_SCALE[canonical_unit(target)]
    LOG.debug("converted %.3f %s into %s", float(value), source, target)
    return round(base / divisor, 6)


def normalize_record(record, unit_fields):
    """Rewrite unit-tagged fields of a record into base units."""
    normalized = dict(record)
    for field, unit in unit_fields.items():
        if field in normalized:
            normalized[field] = to_base(normalized[field], unit)
    return normalized
