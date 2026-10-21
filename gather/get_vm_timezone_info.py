#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Report host timezone settings that affect guest clock consistency."""

import json
import os
import subprocess as sp
import time as t


def _read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read().strip()
    except OSError:
        return ""


def _timedatectl():
    try:
        completed = sp.run(
            "timedatectl show --property=Timezone --value",
            shell=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
        return completed.stdout.strip()
    except (OSError, sp.SubprocessError):
        return ""


report = {
    "time": t.strftime("%Y-%m-%dT%H:%M:%SZ", t.gmtime()),
    "etc_timezone": _read("/etc/timezone"),
    "localtime_link": os.path.realpath("/etc/localtime"),
    "timedatectl_timezone": _timedatectl(),
    "utc": _read("/etc/adjtime").splitlines()[2:3],
}
print(json.dumps(report, indent=2))
