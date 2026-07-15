#!/usr/bin/env python3
"""Parse and format time strings for consistent timestamp handling."""
import re
from datetime import datetime, timedelta
from typing import Optional

class TimeParser:
    """Parses various time string formats."""

    FORMATS = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y/%m/%d %H:%M:%S",
        "%d/%m/%Y %H:%M:%S",
    ]

    @classmethod
    def parse(cls, time_str: str) -> Optional[datetime]:
        """Parse a time string trying multiple formats."""
        for fmt in cls.FORMATS:
            try:
                return datetime.strptime(time_str.strip(), fmt)
            except ValueError:
                continue
        return None

    @staticmethod
    def format(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
        """Format a datetime object to string."""
        return dt.strftime(fmt)

    @staticmethod
    def parse_duration(duration_str: str) -> timedelta:
        """Parse duration string like '1h30m', '45s', '2d'."""
        pattern = re.compile(r"(\d+)([smhdw])")
        matches = pattern.findall(duration_str)
        if not matches:
            return timedelta(0)
        units = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
        total = sum(int(v) * units[u] for v, u in matches)
        return timedelta(seconds=total)

    @staticmethod
    def now_str(fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
        """Return current time as formatted string."""
        return datetime.now().strftime(fmt)
