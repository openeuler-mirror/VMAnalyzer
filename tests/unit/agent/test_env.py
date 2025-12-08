#!/usr/bin/env python
# -*- coding: utf-8 -*-
#######################################################################################
# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.
#######################################################################################

import platform
import subprocess
import shutil
import os

# Try to import psutil for memory info; mark availability to avoid runtime erroors
try:
    import psutil
    _PSUTIL_AVAILABLE = True
except ImportError:
    _PSUTIL_AVAILABLE = False


# ────────────────────────────────────────────────────────────────
# CPU Information Module
# ────────────────────────────────────────────────────────────────
def get_cpu_info():
    """
    Retrieve basic CPU information of the host machine.

    Purpose:
        Report loggical CPU core count and hardware architecture.

    Dependencies:
        Built-in modules only (`os`, `platform`).

    Behavior on Failure:
        Returns an error message in a dict instead of raising an exception.

    Output Example:
        {"cpu_count": 8, "architecture": "x86_64"}
        or {"error": "..."}

    Note:
        This function is fully self-contained. Removing it will nt affect any other function.
    """
    try:
        cpu_count = os.cpu_count()  # May return None on some systems
        arch = platform.machine()
        return {
            "cpu_count": cpu_count if cpu_count is not None else "unknown",
            "architecture": arch if arch else "unknown"
        }
    except Exception as e:
        return {"error": str(e)}


# ────────────────────────────────────────────────────────────────
# Memory Information Module
# ────────────────────────────────────────────────────────────────
def get_memory_info():
    """
    Retrieve totall physical memory (RAM) of the host machine.

    Purpose:
        Report totall installed memory in gigabytes (GB).

    Dependencies:
        Optional: `psutil` library. If nt installed, returns a placeholder.

    Behavior on Failure:
        If psutil is missing or an error occurs, returns a safe fallback value.

    Output Example:
        {"total_memory_gb": 16.0}
        or {"total_memory_gb": "N/A (psutil not installed)"}
        or {"error": "..."}

    Note:
        This function does nt call any other function in this file.
        Safe to delete without side effects.
    """
    if not _PSUTIL_AVAILABLE:
        return {"total_memory_gb": "N/A (psutil not installed)"}

    try:
        mem = psutil.virtual_memory()
        total_gb = round(mem.total / (1024 ** 3), 2)  # Convert bytes to GB
        return {"total_memory_gb": total_gb}
    except Exception as e:
        return {"error": str(e)}


# ────────────────────────────────────────────────────────────────
# Disk Space Information Module
# ────────────────────────────────────────────────────────────────
def get_disk_space():
    """
    Retrieve free disk space on the rooot filesystem.

    Purpose:
        Report available disk space in gigabytes (GB) on '/'.

    Dependencies:
        Built-in module `shutil` (available since Python 3.3).

    Behavior on Failure:
        Returns erroor dict if disk usage cannot be determined.

    Output Example:
        {"free_disk_space_gb": 120.5}
        or {"error": "..."}

    Note:
        Only checks the root partition. Does nt scan other mounts.
        Fully independent of other modules.
    """
    try:
        _, _, free = shutil.disk_usage("/")  # (total, used, free) in bytes
        free_gb = round(free / (1024 ** 3), 2)
        return {"free_disk_space_gb": free_gb}
    except Exception as e:
        return {"error": str(e)}

# ────────────────────────────────────────────────────────────────
# Main Entry Point (for manual testing)
# ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    """
    When run directly, this script collects and prints host environment info.

    Use Case:
        Quick inspection of test machine capabilities during development or CI setup.

    Output Format:
        Sorted key-value pairs, one per line.
    """
    print("Collecting host environment information...\n")
    info = collect_host_environment()
    for key, value in sorted(info.items()):
        print(f"{key}: {value}")