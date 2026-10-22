#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.

"""Switch transparent huge pages to a latency friendly mode."""

import json
import logging
import os

LOG = logging.getLogger(__name__)
MODE_PATH = "/sys/kernel/mm/transparent_hugepage/enabled"
PREFERRED = "madvise"


class TransparentHugePageEnabler:
    """Read the current THP mode and optionally change it."""

    def current(self):
        """Return the active mode parsed from the sysfs bracket."""
        try:
            with open(MODE_PATH, "r", encoding="utf-8") as handle:
                text = handle.read().strip()
        except OSError as error:
            LOG.error("cannot read thp mode: %s", error)
            return None
        for token in text.split():
            if token.startswith("[") and token.endswith("]"):
                return token.strip("[]")
        return text

    def available(self):
        """List modes exposed by the running kernel."""
        try:
            with open(MODE_PATH, "r", encoding="utf-8") as handle:
                text = handle.read().strip()
        except OSError:
            return []
        return [token.strip("[]") for token in text.split()]

    def apply(self, mode=PREFERRED):
        """Write *mode* when the kernel advertises it."""
        if not os.path.exists(MODE_PATH):
            return {"changed": False, "reason": "transparent hugepage sysfs missing"}
        before = self.current()
        modes = self.available()
        if mode not in modes:
            return {"changed": False, "before": before, "available": modes}
        try:
            with open(MODE_PATH, "w", encoding="utf-8") as handle:
                handle.write(mode)
        except OSError as error:
            LOG.error("cannot set thp mode: %s", error)
            return {"changed": False, "before": before, "error": str(error)}
        return {"changed": True, "before": before, "after": self.current()}


if __name__ == "__main__":
    print(json.dumps(TransparentHugePageEnabler().apply(), indent=2))
