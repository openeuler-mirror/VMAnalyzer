#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.

"""Attach dedicated IO threads to domains with heavy disk traffic."""

import json
import logging
import subprocess
import sys

LOG = logging.getLogger(__name__)


class IothreadSetter:
    """Add and optionally pin an IO thread for one domain."""

    def _run(self, command):
        try:
            completed = subprocess.run(
                command, capture_output=True, text=True, timeout=15
            )
        except (OSError, subprocess.SubprocessError) as error:
            LOG.error("command failed: %s", error)
            return None
        if completed.returncode != 0:
            LOG.warning("virsh failed: %s", completed.stderr.strip())
            return None
        return completed.stdout.strip()

    def existing(self, vm_name):
        """Return the current IO thread identifiers for the domain."""
        output = self._run(["virsh", "iothreadinfo", vm_name]) or ""
        threads = []
        for line in output.splitlines():
            fields = line.split()
            if fields and fields[0].rstrip(":").isdigit():
                threads.append(int(fields[0].rstrip(":")))
        return threads

    def apply(self, vm_name, thread_id=1, cpu=None):
        """Add the IO thread and pin it when a CPU is supplied."""
        before = self.existing(vm_name)
        added = self._run(["virsh", "iothreadadd", vm_name, str(thread_id)])
        pinned = None
        if cpu is not None:
            pinned = (
                self._run(
                    ["virsh", "iothreadpin", vm_name, str(thread_id), str(cpu)]
                )
                is not None
            )
        return {
            "vm": vm_name,
            "before": before,
            "added": added is not None,
            "pinned": pinned,
            "after": self.existing(vm_name),
        }


if __name__ == "__main__":
    print(json.dumps(IothreadSetter().apply(sys.argv[1]), indent=2))
