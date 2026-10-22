#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.

"""Cap live migration bandwidth and downtime for predictable cutover."""

import json
import logging
import subprocess

LOG = logging.getLogger(__name__)


class MigrationBandwidthSetter:
    """Apply migration speed and downtime limits through virsh."""

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

    def apply(self, bandwidth_mib=1024, downtime_ms=300):
        """Set both limits and return the observed configuration."""
        speed = self._run(["virsh", "migrate-setspeed", str(bandwidth_mib)])
        downtime = self._run(
            ["virsh", "migrate-setmaxdowntime", str(downtime_ms)]
        )
        current_speed = self._run(["virsh", "migrate-getspeed"])
        return {
            "bandwidth_mib": bandwidth_mib,
            "bandwidth_applied": speed is not None,
            "downtime_ms": downtime_ms,
            "downtime_applied": downtime is not None,
            "observed_speed": current_speed,
            "success": speed is not None and downtime is not None,
        }


if __name__ == "__main__":
    print(json.dumps(MigrationBandwidthSetter().apply(), indent=2))
