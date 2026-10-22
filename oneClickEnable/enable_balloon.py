#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.

"""Check memory balloon availability and compute a safe target size."""

import json
import logging
import subprocess
import sys

LOG = logging.getLogger(__name__)
HEADROOM = 0.2


class BalloonEnabler:
    """Inspect balloon stats and propose a target below current usage."""

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

    def balloon_enabled(self, vm_name):
        """True when the domain XML declares a usable memballoon device."""
        xml = self._run(["virsh", "dumpxml", vm_name]) or ""
        return "memballoon" in xml and "model='none'" not in xml

    def stats(self, vm_name):
        """Parse virsh dommemstat output into a dictionary."""
        output = self._run(["virsh", "dommemstat", vm_name]) or ""
        values = {}
        for line in output.splitlines():
            fields = line.split()
            if len(fields) >= 2:
                try:
                    values[fields[0]] = int(fields[1])
                except ValueError:
                    values[fields[0]] = fields[1]
        return values

    def apply(self, vm_name):
        """Return balloon state and a conservative target in megabytes."""
        stats = self.stats(vm_name)
        actual = stats.get("actual", 0)
        available = stats.get("available", 0)
        target = int(actual * (1.0 - HEADROOM)) if isinstance(actual, int) else 0
        return {
            "vm": vm_name,
            "enabled": self.balloon_enabled(vm_name),
            "actual_kb": actual,
            "available_kb": available,
            "recommended_target_kb": target,
            "stats": stats,
        }


if __name__ == "__main__":
    print(json.dumps(BalloonEnabler().apply(sys.argv[1]), indent=2))
