#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.

"""Add hugepage backed and locked memory to a domain definition."""

import json
import logging
import os
import subprocess
import tempfile

LOG = logging.getLogger(__name__)
BACKING = "<memoryBacking>\n  <hugepages/>\n  <locked/>\n</memoryBacking>\n"


class MemoryBackingSetter:
    """Prepare a memoryBacking block and optionally redefine the domain."""

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

    def domain_xml(self, vm_name):
        """Return the live domain XML, or None when virsh fails."""
        xml = self._run(["virsh", "dumpxml", vm_name])
        if not xml:
            LOG.error("cannot dump xml for %s", vm_name)
        return xml

    def audit(self, vm_name):
        """Report whether the domain already requests explicit backing."""
        xml = self.domain_xml(vm_name) or ""
        return {
            "vm": vm_name,
            "has_memory_backing": "<memoryBacking>" in xml,
            "uses_hugepages": "<hugepages" in xml,
            "locked": "<locked" in xml,
        }

    def apply(self, vm_name, confirm=False):
        """Build the updated definition and define it when confirmed."""
        xml = self.domain_xml(vm_name)
        if not xml:
            return {"vm": vm_name, "changed": False, "reason": "no domain xml"}
        if "<memoryBacking>" in xml:
            return {"vm": vm_name, "changed": False, "reason": "already configured"}
        updated = xml.replace("</domain>", BACKING + "</domain>")
        if not confirm:
            return {"vm": vm_name, "changed": False, "preview": BACKING}
        path = None
        try:
            with tempfile.NamedTemporaryFile(
                "w", suffix=".xml", delete=False, encoding="utf-8"
            ) as handle:
                path = handle.name
                handle.write(updated)
            defined = self._run(["virsh", "define", path]) is not None
        finally:
            if path and os.path.exists(path):
                os.unlink(path)
        return {"vm": vm_name, "changed": defined}


if __name__ == "__main__":
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else ""
    print(json.dumps(MemoryBackingSetter().audit(target), indent=2))
