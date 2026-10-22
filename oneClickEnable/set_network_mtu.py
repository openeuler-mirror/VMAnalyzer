#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.

"""Raise bridge MTU so guests can use jumbo frames."""

import json
import logging
import re
import subprocess
import sys

LOG = logging.getLogger(__name__)
MTU = re.compile(r"mtu (\d+)")


class NetworkMtuSetter:
    """Inspect domain interfaces and adjust their host bridge MTU."""

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

    def sources(self, vm_name):
        """Return the host network sources attached to the domain."""
        output = self._run(["virsh", "domiflist", vm_name]) or ""
        sources = []
        for line in output.splitlines()[2:]:
            fields = line.split()
            if len(fields) >= 2 and fields[1] not in sources:
                sources.append(fields[1])
        return sources

    def current_mtu(self, device):
        """Read the configured MTU for one device."""
        output = self._run(["ip", "-o", "link", "show", "dev", device]) or ""
        match = MTU.search(output)
        return int(match.group(1)) if match else None

    def apply(self, vm_name, mtu=9000, confirm=False):
        """Plan or perform MTU changes for every attached source."""
        changes = []
        for device in self.sources(vm_name):
            before = self.current_mtu(device)
            changed = False
            if confirm and before is not None and before != mtu:
                changed = (
                    self._run(
                        ["ip", "link", "set", "dev", device, "mtu", str(mtu)]
                    )
                    is not None
                )
            changes.append(
                {
                    "device": device,
                    "before": before,
                    "target": mtu,
                    "changed": changed,
                }
            )
        return {"vm": vm_name, "mtu": mtu, "changes": changes}


if __name__ == "__main__":
    print(json.dumps(NetworkMtuSetter().apply(sys.argv[1]), indent=2))
