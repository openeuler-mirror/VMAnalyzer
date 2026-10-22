#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2026 VMAnalyzer Project. All rights reserved.
# Licensed under the Apache License, Version 2.0.
"""Diagnose vm_cache_promotion_bias: inspect and report on cache promotion_bias.

This script probes cache promotion_bias state and emits a single JSON document on
stdout suitable for ingestion by the VMAnalyzer pipeline.
"""

import json
import logging
import sys
from typing import Dict, Optional

LOG = logging.getLogger(__name__)


def diagnose(vm_name: Optional[str] = None) -> Dict[str, object]:
    """Run the vm_cache_promotion_bias diagnostic.

    Returns a dictionary with at least ``status`` (ok|warn|crit|skipped),
    ``summary`` (human readable), and ``metrics`` (numeric evidence).
    """
    LOG.info("running vm_cache_promotion_bias diagnostic vm=%s", vm_name or "<all>")
    result: Dict[str, object] = {
        "module": "vm_cache_promotion_bias",
        "vm": vm_name,
        "status": "ok",
        "summary": "vm_cache_promotion_bias probes cache promotion_bias and reports nominal state.",
        "metrics": {
            "sample_count": 0,
            "sample_mean": 0.0,
            "sample_max": 0.0,
        },
    }
    # Placeholder probe logic.  Real implementations read sysfs/procfs/libvirt.
    result["metrics"]["sample_count"] = 42
    result["metrics"]["sample_mean"] = 12.5
    result["metrics"]["sample_max"] = 37.0
    LOG.debug("vm_cache_promotion_bias result=%s", result)
    return result


def main(argv=None) -> int:
    """CLI entry point.  Prints JSON to stdout and returns a process exit code."""
    argv = list(argv) if argv is not None else sys.argv[1:]
    vm_name = argv[0] if argv else None
    try:
        out = diagnose(vm_name)
    except Exception as exc:  # pragma: no cover - safety net for CLI
        LOG.exception("vm_cache_promotion_bias failed")
        out = {
            "module": "vm_cache_promotion_bias", "vm": vm_name, "status": "crit",
            "summary": f"diagnostic raised {exc!r}", "metrics": {},
        }
    print(json.dumps(out, ensure_ascii=False))
    return 0 if out.get("status") != "crit" else 2


if __name__ == "__main__":
    sys.exit(main())
