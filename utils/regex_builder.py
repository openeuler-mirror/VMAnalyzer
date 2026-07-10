#!/usr/bin/env python3
"""Regex pattern builder for fluent regex construction."""
import re
from typing import List, Optional

class RegexBuilder:
    def __init__(self):
        self._parts: List[str] = []

    def literal(self, text: str) -> "RegexBuilder":
        self._parts.append(re.escape(text))
        return self

    def any_of(self, chars: str) -> "RegexBuilder":
        self._parts.append(f"[{chars}]")
        return self

    def digit(self) -> "RegexBuilder":
        self._parts.append(r"\d")
        return self

    def word_char(self) -> "RegexBuilder":
        self._parts.append(r"\w")
        return self

    def whitespace(self) -> "RegexBuilder":
        self._parts.append(r"\s")
        return self

    def repeat(self, min_n: int, max_n: int = None) -> "RegexBuilder":
        if max_n is None:
            self._parts.append(f"{{{min_n},}}")
        elif min_n == max_n:
            self._parts.append(f"{{{min_n}}}")
        else:
            self._parts.append(f"{{{min_n},{max_n}}}")
        return self

    def optional(self) -> "RegexBuilder":
        self._parts.append("?")
        return self

    def one_or_more(self) -> "RegexBuilder":
        self._parts.append("+")
        return self

    def group(self) -> "RegexBuilder":
        self._parts.insert(0, "(")
        self._parts.append(")")
        return self

    def anchor_start(self) -> "RegexBuilder":
        self._parts.insert(0, "^")
        return self

    def anchor_end(self) -> "RegexBuilder":
        self._parts.append("$")
        return self

    def build(self) -> str:
        return "".join(self._parts)

    def compile(self, flags=0):
        return re.compile(self.build(), flags)

    def matches(self, text: str) -> bool:
        return bool(re.search(self.build(), text))

    def find_all(self, text: str) -> List[str]:
        return re.findall(self.build(), text)
