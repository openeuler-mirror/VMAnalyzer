#!/usr/bin/env python3
"""Text parser with tokenizer for structured text extraction."""
import re
from typing import List, Dict, Optional

class Token:
    def __init__(self, kind: str, value: str):
        self.kind = kind
        self.value = value
    def __repr__(self): return f"Token({self.kind}, {self.value!r})"

class TextParser:
    def __init__(self):
        self._patterns: List[tuple] = []

    def add_pattern(self, name: str, pattern: str) -> None:
        self._patterns.append((name, re.compile(pattern)))

    def tokenize(self, text: str) -> List[Token]:
        tokens = []
        pos = 0
        while pos < len(text):
            matched = False
            for name, regex in self._patterns:
                m = regex.match(text, pos)
                if m:
                    tokens.append(Token(name, m.group()))
                    pos = m.end()
                    matched = True
                    break
            if not matched:
                tokens.append(Token("UNKNOWN", text[pos]))
                pos += 1
        return tokens

    def extract_pairs(self, text: str, opener: str, closer: str) -> List[str]:
        results = []
        depth = 0
        start = -1
        for i, ch in enumerate(text):
            if ch == opener:
                if depth == 0:
                    start = i
                depth += 1
            elif ch == closer and depth > 0:
                depth -= 1
                if depth == 0 and start >= 0:
                    results.append(text[start+1:i])
                    start = -1
        return results
