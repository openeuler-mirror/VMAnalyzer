#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.

"""Review virtio queue sizes and suggest jumbo ring settings."""

import json
import logging
import re
import subprocess
import sys

LOG = logging.getLogger(__name__)
RX = re.compile(r"rx_queue_size='(\d+)'")
TX = re.compile(r"tx_queue_size='(\d+)'")


class VirtioRingTuner:
    """Compare ring sizes with a vCPU based recommendation."""

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
        """Return the active vCPU count for sizing the rings."""
        output = self._run(["virsh", "vcpucount", vm_name, "--active"])
        return int(output) if output and output.isdigit() else 0

    def recommend(self, vcpus):
        """Pick a ring size that grows with vCPU pressure."""
        size = 1024 if vcpus >= 8 else 256
        return {"rx_queue_size": size, "tx_queue_size": size}

    def apply(self, vm_name):
        """Report current ring sizes next to the recommendation."""
        xml = self._run(["virsh", "dumpxml", vm_name]) or ""
        vcpus = self.vcpu_count(vm_name)
        current = {
            "rx_queue_size": [int(value) for value in RX.findall(xml)],
            "tx_queue_size": [int(value) for value in TX.findall(xml)],
        }
        advice = self.recommend(vcpus)
        outdated = any(
            value < advice["rx_queue_size"] for value in current["rx_queue_size"]
        )
        return {
            "vm": vm_name,
            "vcpus": vcpus,
            "current": current,
            "recommended": advice,
            "needs_tuning": outdated,
        }


if __name__ == "__main__":
    print(json.dumps(VirtioRingTuner().apply(sys.argv[1]), indent=2))
