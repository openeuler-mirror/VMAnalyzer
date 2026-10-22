#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the
# Mulan PSL v2.

"""Enable irqbalance so interrupt load follows the pinned vCPU layout."""

import json
import logging
import subprocess

LOG = logging.getLogger(__name__)


class IrqBalanceEnabler:
    """Ensure the irqbalance service is installed, enabled and running."""

    def _run(self, command):
        try:
            completed = subprocess.run(
                command, capture_output=True, text=True, timeout=15
            )
        except (OSError, subprocess.SubprocessError) as error:
            LOG.error("command failed: %s", error)
            return None
        if completed.returncode != 0:
            LOG.warning("command failed: %s", completed.stderr.strip())
            return None
        return completed.stdout.strip()

    def status(self):
        """Return the current active and enabled service state."""
        return {
            "active": self._run(["systemctl", "is-active", "irqbalance"]) or "unknown",
            "enabled": self._run(["systemctl", "is-enabled", "irqbalance"]) or "unknown",
        }

    def apply(self):
        """Enable and start irqbalance, reporting every attempted action."""
        before = self.status()
        actions = []
        if before["enabled"] not in ("enabled", "static"):
            ok = self._run(["systemctl", "enable", "irqbalance"]) is not None
            actions.append({"action": "enable", "success": ok})
        if before["active"] != "active":
            ok = self._run(["systemctl", "start", "irqbalance"]) is not None
            actions.append({"action": "start", "success": ok})
        return {"before": before, "actions": actions, "after": self.status()}


if __name__ == "__main__":
    print(json.dumps(IrqBalanceEnabler().apply(), indent=2))
