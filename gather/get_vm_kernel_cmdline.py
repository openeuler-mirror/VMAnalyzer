#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Parse kernel boot parameters relevant to virtualisation tuning."""

import json
import time as t

INTERESTING = (
    "iommu",
    "intel_iommu",
    "amd_iommu",
    "hugepages",
    "default_hugepagesz",
    "isolcpus",
    "nohz_full",
    "rcu_nocbs",
    "transparent_hugepage",
)


def _read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read().strip()
    except OSError:
        return ""


tokens = _read("/proc/cmdline").split()
parameters = {}
for token in tokens:
    key, _, value = token.partition("=")
    parameters[key] = value or True
matched = [token for token in tokens if any(flag in token for flag in INTERESTING)]
report = {
    "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
    "token_count": len(tokens),
    "parameters": parameters,
    "virtualisation_flags": matched,
}
print(json.dumps(report, indent=2))
