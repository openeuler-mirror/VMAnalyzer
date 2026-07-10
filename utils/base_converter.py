#!/usr/bin/env python3
"""Number base converter supporting arbitrary bases."""
from typing import str

DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def to_base(num: int, base: int) -> str:
    if base < 2 or base > 36:
        raise ValueError("Base must be between 2 and 36")
    if num == 0:
        return "0"
    negative = num < 0
    num = abs(num)
    result = []
    while num > 0:
        result.append(DIGITS[num % base])
        num //= base
    if negative:
        result.append("-")
    return "".join(reversed(result))

def from_base(s: str, base: int) -> int:
    if base < 2 or base > 36:
        raise ValueError("Base must be between 2 and 36")
    s = s.strip().upper()
    negative = False
    if s.startswith("-"):
        negative = True
        s = s[1:]
    result = 0
    for ch in s:
        val = DIGITS.index(ch)
        if val >= base:
            raise ValueError(f"Invalid digit {ch} for base {base}")
        result = result * base + val
    return -result if negative else result

def convert(s: str, from_base: int, to_base: int) -> str:
    return to_base(from_base(s, from_base), to_base)
