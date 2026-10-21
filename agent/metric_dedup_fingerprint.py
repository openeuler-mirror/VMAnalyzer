#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Fingerprints for detecting duplicate metric payloads."""

import hashlib
import logging

LOG = logging.getLogger(__name__)


def fingerprint(payload, keys=None):
    """Hash the selected payload fields into a short identifier."""
    if keys is not None:
        text = "|".join(str(payload.get(key, "")) for key in sorted(keys))
    else:
        text = str(sorted(payload.items()))
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:16]


class Deduplicator:
    """Remember recent fingerprints and reject repeats."""

    def __init__(self, capacity=1024):
        self.capacity = int(capacity)
        self._seen = []
        self.duplicates = 0

    def is_duplicate(self, payload, keys=None):
        """Return True when the payload fingerprint was seen recently."""
        token = fingerprint(payload, keys)
        if token in self._seen:
            self.duplicates += 1
            LOG.debug("duplicate payload %s", token)
            return True
        self._seen.append(token)
        if len(self._seen) > self.capacity:
            del self._seen[0]
        return False
