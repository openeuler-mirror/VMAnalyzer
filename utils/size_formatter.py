#!/usr/bin/env python3
"""Format byte sizes into human-readable strings."""
from typing import Tuple

class SizeFormatter:
    """Formats byte counts into human-readable strings."""

    UNITS = ["B", "KB", "MB", "GB", "TB", "PB"]
    BINARY_UNITS = ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]

    @classmethod
    def format(cls, size: int, binary: bool = False) -> str:
        """Format byte size to human-readable string."""
        units = cls.BINARY_UNITS if binary else cls.UNITS
        base = 1024 if binary else 1000
        if size < 0:
            return "-" + cls.format(-size, binary)
        if size == 0:
            return "0 B"
        for unit in units:
            if abs(size) < base:
                return f"{size:.1f} {unit}"
            size /= base
        return f"{size:.1f} {units[-1]}"

    @classmethod
    def parse(cls, size_str: str) -> int:
        """Parse a human-readable size string to bytes."""
        size_str = size_str.strip().upper()
        for i, unit in enumerate(cls.UNITS):
            if size_str.endswith(unit):
                num = float(size_str[:-len(unit)].strip())
                return int(num * (1000 ** i))
        return int(size_str)

    @classmethod
    def to_bytes(cls, value: float, unit: str) -> int:
        """Convert value in given unit to bytes."""
        unit = unit.upper()
        if unit in cls.UNITS:
            return int(value * (1000 ** cls.UNITS.index(unit)))
        if unit in cls.BINARY_UNITS:
            return int(value * (1024 ** cls.BINARY_UNITS.index(unit)))
        return int(value)
