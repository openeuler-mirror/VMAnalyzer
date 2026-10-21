#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Normalise VM labels used in metric names."""

import logging
import re

LOG = logging.getLogger(__name__)
INVALID = re.compile(r"[^a-z0-9_.-]+")


def normalize_label(name):
    """Lowercase and slugify a VM label."""
    if not name:
        return "unknown"
    slug = INVALID.sub("_", name.strip().lower()).strip("_")
    return slug or "unknown"


def normalize_labels(labels):
    """Normalise each label value while keeping the keys intact."""
    return {key: normalize_label(value) for key, value in labels.items()}


def dedupe_labels(labels):
    """Add a numeric suffix when normalisation collapses two labels."""
    seen = {}
    result = {}
    for key, value in labels.items():
        slug = normalize_label(value)
        count = seen.get(slug, 0) + 1
        seen[slug] = count
        result[key] = slug if count == 1 else "{}_{}".format(slug, count)
    LOG.debug("deduplicated %d labels", len(result))
    return result
