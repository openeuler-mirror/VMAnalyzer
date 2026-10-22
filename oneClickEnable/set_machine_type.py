#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.

"""Compare a domain machine type with machine types the host supports."""

import json
import logging
import re
import subprocess
import sys

LOG = logging.getLogger(__name__)
MACHINE = re.compile(r"<type[^>]*machine='([^']+)'")


class MachineTypeSetter:
    """Audit whether the guest uses an available modern machine type."""

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

    def host_machines(self):
        """List machine types reported by domcapabilities."""
        output = self._run(["virsh", "domcapabilities"]) or ""
        return sorted({match for match in re.findall(r"'machine': '([^']+)'", output)})

    def domain_machine(self, vm_name):
        """Return the machine type recorded in the domain XML."""
        xml = self._run(["virsh", "dumpxml", vm_name]) or ""
        match = MACHINE.search(xml)
        return match.group(1) if match else None

    def apply(self, vm_name):
        """Report availability and whether a newer type could be chosen."""
        machines = self.host_machines()
        current = self.domain_machine(vm_name)
        modern = [item for item in machines if "q35" in item or "virt" in item]
        return {
            "vm": vm_name,
            "machine": current,
            "available_count": len(machines),
            "modern_candidates": modern[:10],
            "supported": current in machines if current else False,
        }


if __name__ == "__main__":
    print(json.dumps(MachineTypeSetter().apply(sys.argv[1]), indent=2))
