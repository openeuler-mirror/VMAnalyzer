#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.

"""Shut a guest down with a bounded wait and optional forced power off."""

import json
import logging
import subprocess
import sys
import time

LOG = logging.getLogger(__name__)


class ShutdownTimeoutSetter:
    """Send ACPI shutdown, poll the state and enforce a timeout."""

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

    def state(self, vm_name):
        """Current runstate reported by virsh."""
        return self._run(["virsh", "domstate", vm_name]) or "unknown"

    def apply(self, vm_name, timeout=60, force=False):
        """Request shutdown and report whether it completed in time."""
        started = time.time()
        sent = self._run(["virsh", "shutdown", vm_name]) is not None
        state = self.state(vm_name)
        while sent and state == "running" and time.time() - started < timeout:
            time.sleep(2)
            state = self.state(vm_name)
        forced = False
        if state == "running" and force:
            forced = self._run(["virsh", "destroy", vm_name]) is not None
            state = self.state(vm_name)
        return {
            "vm": vm_name,
            "timeout": timeout,
            "shutdown_sent": sent,
            "forced": forced,
            "final_state": state,
            "elapsed": round(time.time() - started, 2),
        }


if __name__ == "__main__":
    print(json.dumps(ShutdownTimeoutSetter().apply(sys.argv[1]), indent=2))
