#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2026 VMAnalyzer Authors. All rights reserved.
"""iopl privileges"""
import json
import logging
import os
import sys

LOG = logging.getLogger(__name__)
def _collect() -> Dict[str, Any]:
    """Run a platform-appropriate collection."""
    info: Dict[str, Any] = {}
    try:
        with open("/proc/meminfo", "r", encoding="utf-8", errors="ignore") as fh:
            info["raw"] = fh.read().strip()
    except FileNotFoundError:
        info["raw"] = ""
    except OSError as exc:
        LOG.warning("read failed: %s", exc)
        info["raw"] = ""
    return info

def diagnose() -> Dict[str, Any]:
    """Return a JSON-serialisable diagnosis result."""
    return {
        "module": "get_vm_iopl",
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
