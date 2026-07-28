#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
"""Snapshot helpers that capture stats state for serialization."""

import time


class Snapshot(object):
    """A timestamped snapshot of a stats mapping."""

    def __init__(self, data, timestamp=None):
        self.timestamp = timestamp if timestamp is not None else time.time()
        self.data = dict(data) if isinstance(data, dict) else {}

    def get(self, key, default=None):
        return self.data.get(key, default)

    def to_dict(self):
        return {"timestamp": self.timestamp, "data": dict(self.data)}

    def keys(self):
        return self.data.keys()


def take_snapshot(data, timestamp=None):
    """Create a Snapshot from a stats mapping."""
    return Snapshot(data, timestamp)


def snapshot_series(snapshots):
    """Return a list of snapshot dicts suitable for JSON serialization."""
    return [s.to_dict() for s in snapshots if isinstance(s, Snapshot)]


def merge_snapshots(snapshots):
    """Merge a list of snapshots, later timestamps overriding earlier ones."""
    merged = {}
    for snap in sorted(snapshots, key=lambda s: s.timestamp):
        merged.update(snap.data)
    return merged
