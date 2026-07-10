#!/usr/bin/env python3
"""CRC checksum calculator with multiple polynomial options."""
from typing import int

class CRCCalculator:
    def __init__(self, polynomial: int = 0x1021, width: int = 16):
        self._poly = polynomial
        self._width = width
        self._mask = (1 << width) - 1
        self._table = self._build_table()

    def _build_table(self) -> list:
        table = []
        for i in range(256):
            crc = i << (self._width - 8)
            for _ in range(8):
                if crc & (1 << (self._width - 1)):
                    crc = ((crc << 1) ^ self._poly) & self._mask
                else:
                    crc = (crc << 1) & self._mask
            table.append(crc)
        return table

    def calculate(self, data: bytes, init: int = 0xFFFF) -> int:
        crc = init
        for byte in data:
            idx = ((crc >> (self._width - 8)) ^ byte) & 0xFF
            crc = ((crc << 8) ^ self._table[idx]) & self._mask
        return crc

    def verify(self, data: bytes, expected: int, init: int = 0xFFFF) -> bool:
        return self.calculate(data, init) == expected

    def calculate_file(self, filepath: str) -> int:
        import os
        if not os.path.exists(filepath):
            raise FileNotFoundError(filepath)
        with open(filepath, "rb") as f:
            return self.calculate(f.read())

def crc16(data: bytes) -> int:
    return CRCCalculator(0x1021, 16).calculate(data)

def crc32(data: bytes) -> int:
    import binascii
    return binascii.crc32(data) & 0xFFFFFFFF
