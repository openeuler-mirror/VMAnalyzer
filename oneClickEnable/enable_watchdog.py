#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.

"""Attach a virtual watchdog device so guests recover from hangs."""

import json
import logging
import os
import subprocess
import sys
import tempfile

LOG = logging.getLogger(__name__)
DEVICE = "<watchdog model='i6300esb' action='reset'/>\n"


class WatchdogEnabler:
    """Add a watchdog device to domains that do not define one."""

    def _run(self, command):
        try:
            completed = subprocess.run(
                command, capture_output=True, text=True, timeout=20
            )
        except (OSError, subprocess.SubprocessError) as error:
            LOG.error("command failed: %s", error)
            return None
        if completed.returncode != 0:
            return None
        return completed.stdout.strip()

    def has_watchdog(self, vm_name):
        """True when the live XML already contains a watchdog."""
        xml = self._run(["virsh", "dumpxml", vm_name]) or ""
        return "<watchdog" in xml

    def apply(self, vm_name, confirm=False):
        """Attach the watchdog device when requested and absent."""
        if self.has_watchdog(vm_name):
            return {"vm": vm_name, "changed": False, "reason": "already present"}
        if not confirm:
            return {"vm": vm_name, "changed": False, "preview": DEVICE.strip()}
        path = None
        try:
            with tempfile.NamedTemporaryFile(
                "w", suffix=".xml", delete=False, encoding="utf-8"
            ) as handle:
                path = handle.name
                handle.write(DEVICE)
            attached = (
                self._run(
                    ["virsh", "attach-device", vm_name, path, "--config"]
                )
                is not None
            )
        finally:
            if path and os.path.exists(path):
                os.unlink(path)
        return {"vm": vm_name, "changed": attached}


if __name__ == "__main__":
    print(json.dumps(WatchdogEnabler().apply(sys.argv[1]), indent=2))
