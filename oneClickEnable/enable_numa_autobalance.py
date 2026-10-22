#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.

"""Enable automatic NUMA balancing for better memory locality."""

import json
import logging

LOG = logging.getLogger(__name__)
SYSCTL_PATH = "/proc/sys/kernel/numa_balancing"


class NumaAutoBalanceEnabler:
    """Toggle kernel NUMA balancing and report the observed state."""

    def current(self):
        """Return the raw sysctl value, or None when unavailable."""
        try:
            with open(SYSCTL_PATH, "r", encoding="utf-8") as handle:
                return handle.read().strip()
        except OSError as error:
            LOG.error("cannot read numa balancing: %s", error)
            return None

    def apply(self, value=1):
        """Write the requested value and confirm it took effect."""
        before = self.current()
        if before is None:
            return {"changed": False, "reason": "numa balancing sysctl missing"}
        try:
            with open(SYSCTL_PATH, "w", encoding="utf-8") as handle:
                handle.write(str(int(value)))
        except OSError as error:
            LOG.error("cannot set numa balancing: %s", error)
            return {"changed": False, "before": before, "error": str(error)}
        after = self.current()
        return {
            "changed": before != after,
            "before": before,
            "after": after,
            "recommended": after == "1",
        }


if __name__ == "__main__":
    print(json.dumps(NumaAutoBalanceEnabler().apply(), indent=2))
