#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.

"""Align the domain CPU topology with the configured vCPU count."""

import json
import logging
import re
import subprocess
import sys

LOG = logging.getLogger(__name__)
TOPOLOGY = re.compile(r"<topology[^>]*sockets='(\d+)'[^>]*cores='(\d+)'")


class VcpuTopologySetter:
    """Compare declared sockets and cores against the vCPU count."""

    def _run(self, command):
        try:
            completed = subprocess.run(
                command, capture_output=True, text=True, timeout=15
            )
        except (OSError, subprocess.SubprocessError) as error:
            LOG.error("command failed: %s", error)
            return None
        if completed.returncode != 0:
            return None
        return completed.stdout.strip()

    def vcpu_count(self, vm_name):
        """Return the active vCPU count reported by virsh."""
        output = self._run(["virsh", "vcpucount", vm_name, "--active"])
        return int(output) if output and output.isdigit() else 0

    def topology(self, vm_name):
        """Extract sockets, cores and threads from the domain XML."""
        xml = self._run(["virsh", "dumpxml", vm_name]) or ""
        match = TOPOLOGY.search(xml)
        if not match:
            return None
        sockets = int(match.group(1))
        cores = int(match.group(2))
        threads_match = re.search(r"threads='(\d+)'", match.group(0))
        threads = int(threads_match.group(1)) if threads_match else 1
        return {"sockets": sockets, "cores": cores, "threads": threads}

    def recommended(self, count):
        """Pick a balanced topology with one thread per core."""
        cores = min(max(1, count), 8)
        sockets = max(1, count // cores)
        return {"sockets": sockets, "cores": cores, "threads": 1}

    def apply(self, vm_name):
        """Report the mismatch between declared and recommended topology."""
        count = self.vcpu_count(vm_name)
        declared = self.topology(vm_name)
        advice = self.recommended(count)
        consistent = bool(declared) and (
            declared["sockets"] * declared["cores"] * declared["threads"] == count
        )
        return {
            "vm": vm_name,
            "vcpus": count,
            "declared": declared,
            "recommended": advice,
            "consistent": consistent,
        }


if __name__ == "__main__":
    print(json.dumps(VcpuTopologySetter().apply(sys.argv[1]), indent=2))
