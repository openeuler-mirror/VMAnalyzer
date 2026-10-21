#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.

"""Verify vhost-net acceleration is usable by tap backed guests."""

import json
import logging
import os
import subprocess

LOG = logging.getLogger(__name__)


class VhostNetEnabler:
    """Load vhost_net when needed and report per-domain usage."""

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

    def kernel_ready(self):
        """Report whether the device node and module are present."""
        try:
            with open("/proc/modules", "r", encoding="utf-8") as handle:
                modules = handle.read()
        except OSError:
            modules = ""
        return {
            "device_node": os.path.exists("/dev/vhost-net"),
            "module_loaded": "vhost_net" in modules,
        }

    def ensure(self):
        """Load the module when it is missing from the running kernel."""
        before = self.kernel_ready()
        loaded = None
        if not before["module_loaded"]:
            loaded = self._run(["modprobe", "vhost_net"]) is not None
        return {"before": before, "modprobe": loaded, "after": self.kernel_ready()}

    def domains(self):
        """Count interfaces that request the vhost driver."""
        names = (self._run(["virsh", "list", "--name"]) or "").split()
        usage = {}
        for name in names:
            xml = self._run(["virsh", "dumpxml", name]) or ""
            usage[name] = xml.count("<driver name='vhost'")
        return {"domain_count": len(names), "vhost_interfaces": usage}

    def apply(self):
        """Return one report combining kernel readiness and domain usage."""
        result = self.ensure()
        result.update(self.domains())
        return result


if __name__ == "__main__":
    print(json.dumps(VhostNetEnabler().apply(), indent=2))
