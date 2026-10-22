#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2026 VMAnalyzer Authors. All rights reserved.
"""filesystem type per mount"""
import json
import logging
import os
import sys

LOG = logging.getLogger(__name__)
def _collect() -> Dict[str, Any]:
    """Collect filesystem-level metrics."""
    out: Dict[str, Any] = {}
    with open("/proc/mounts", "r", encoding="utf-8") as fh:
        out["mounts"] = [ln.strip() for ln in fh if ln.strip()]
    return out

def diagnose() -> Dict[str, Any]:
    """Return a JSON-serialisable diagnosis result."""
    return {
        "module": "get_vm_fs_type",
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
