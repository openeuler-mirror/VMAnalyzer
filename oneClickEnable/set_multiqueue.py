#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.

"""Recommend virtio multiqueue settings from the active vCPU count."""

import json
import logging
import re
import subprocess
import sys

LOG = logging.getLogger(__name__)
QUEUES = re.compile(r"queues='(\d+)'")
MAX_QUEUES = 8


class MultiqueueSetter:
    """Audit virtio queue counts and suggest the vCPU aligned value."""

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
        """Return the number of active vCPUs."""
        output = self._run(["virsh", "vcpucount", vm_name, "--active"])
        return int(output) if output and output.isdigit() else 0

    def recommended(self, vcpus):
        """Keep one queue per vCPU, capped by the virtio limit."""
        return max(1, min(vcpus, MAX_QUEUES))

    def apply(self, vm_name):
        """Compare declared queues with the recommendation."""
        vcpus = self.vcpu_count(vm_name)
        xml = self._run(["virsh", "dumpxml", vm_name]) or ""
        declared = [int(value) for value in QUEUES.findall(xml)]
        target = self.recommended(vcpus)
        mismatched = [value for value in declared if value < target]
        return {
            "vm": vm_name,
            "vcpus": vcpus,
            "declared_queues": declared,
            "recommended_queues": target,
            "mismatched": mismatched,
            "needs_update": bool(mismatched),
        }


if __name__ == "__main__":
    print(json.dumps(MultiqueueSetter().apply(sys.argv[1]), indent=2))
