"""Parse fixed-width column data using explicit slice boundaries."""
from dataclasses import dataclass

__all__ = ["ColumnSpan", "parse_fixed_width"]


@dataclass(frozen=True)
class ColumnSpan:
    """A named half-open character range within a fixed-width record."""

    name: str
    start: int
    end: int

    def slice_of(self, line):
        """Return the stripped content of this span within *line*."""
        return str(line)[self.start:self.end].strip()


def parse_fixed_width(lines, spans):
    """Parse *lines* into dicts keyed by each span's name."""
    return [{span.name: span.slice_of(line) for span in spans} for line in lines]
