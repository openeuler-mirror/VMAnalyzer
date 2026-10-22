#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2026 VMAnalyzer Authors. All rights reserved.
"""read disk queue stats"""
import json
import logging
import os
import sys

LOG = logging.getLogger(__name__)
def _collect() -> Dict[str, Any]:
    """Collect blkio controller statistics."""
    out: Dict[str, Any] = {}
    for path in ("/sys/fs/cgroup/blkio/blkio.throttle.io_service_bytes",
                 "/sys/block", "/proc/diskstats"):
        if os.path.exists(path):
            if os.path.isdir(path):
                out[path] = sorted(os.listdir(path))
            else:
                with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                    out[path] = fh.read().strip()
        else:
            out[path] = None
    return out

def diagnose() -> Dict[str, Any]:
    """Return a JSON-serialisable diagnosis result."""
    return {
        "module": "get_vm_disk_queue",
        "ok": True,
        "data": _collect(),
    }


def main() -> int:
    """CLI entry point."""
    logging.basicConfig(level=logging.INFO)
    print(json.dumps(diagnose(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
