#!/usr/bin/env python3
"""Simple CSV file writer with fluent interface."""
import csv
from typing import Any, List

class CSVWriter:
    """Writes data to CSV files with header support."""

    def __init__(self, filepath: str, headers: List[str] = None):
        self._filepath = filepath
        self._headers = headers
        self._file = None
        self._writer = None

    def open(self) -> "CSVWriter":
        self._file = open(self._filepath, "w", newline="", encoding="utf-8")
        self._writer = csv.writer(self._file)
        if self._headers:
            self._writer.writerow(self._headers)
        return self

    def write_row(self, row: List[Any]) -> "CSVWriter":
        if self._writer:
            self._writer.writerow(row)
        return self

    def write_rows(self, rows: List[List[Any]]) -> "CSVWriter":
        for row in rows:
            self.write_row(row)
        return self

    def write_dict(self, data: dict) -> "CSVWriter":
        if self._headers:
            self.write_row([data.get(h, "") for h in self._headers])
        return self

    def close(self) -> None:
        if self._file:
            self._file.close()
            self._file = None
