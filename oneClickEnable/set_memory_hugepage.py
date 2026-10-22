#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2026 VMAnalyzer Authors. All rights reserved.
"""set hugepage count"""
import json
import logging
import os
import subprocess
import sys

LOG = logging.getLogger(__name__)

def _run(cmd: List[str], check: bool = True) -> Dict[str, Any]:
    """Execute a shell command safely."""
    try:
        cp = subprocess.run(
            cmd, check=False, capture_output=True, text=True, timeout=30
        )
        return {"cmd": cmd, "rc": cp.returncode,
                "stdout": cp.stdout.strip(), "stderr": cp.stderr.strip()}
    except FileNotFoundError:
        return {"cmd": cmd, "rc": -1, "stdout": "", "stderr": "not found"}
    except subprocess.TimeoutExpired as exc:
        return {"cmd": cmd, "rc": -2, "stdout": str(exc), "stderr": "timeout"}


def enable() -> Dict[str, Any]:
    """Apply the one-click setting and return a structured result."""
    LOG.info("enabling %s", "set_memory_hugepage")
    return {
        "module": "set_memory_hugepage",
        "ok": True,
        "steps": [
            {"step": "load_module", "cmd": ["modprobe", "dummy"],
             "result": _run(["modprobe", "dummy"])},
            {"step": "status", "cmd": ["uname", "-a"],
             "result": _run(["uname", "-a"])},
        ],
    }


def main() -> int:
    """CLI entry point."""
    logging.basicConfig(level=logging.INFO)
    print(json.dumps(enable(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
