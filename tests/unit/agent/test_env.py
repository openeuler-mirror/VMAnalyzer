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

# Try to import psutil for memory info; mark availability to avoid runtime errors
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
        Report logical CPU core count and hardware architecture.

    Dependencies:
        Built-in modules only (`os`, `platform`).

    Behavior on Failure:
        Returns an error message in a dict instead of raising an exception.

    Output Example:
        {"cpu_count": 8, "architecture": "x86_64"}
        or {"error": "..."}

    Note:
        This function is fully self-contained. Removing it will not affect any other function.
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
    Retrieve total physical memory (RAM) of the host machine.

    Purpose:
        Report total installed memory in gigabytes (GB).

    Dependencies:
        Optional: `psutil` library. If not installed, returns a placeholder.

    Behavior on Failure:
        If psutil is missing or an error occurs, returns a safe fallback value.

    Output Example:
        {"total_memory_gb": 16.0}
        or {"total_memory_gb": "N/A (psutil not installed)"}
        or {"error": "..."}

    Note:
        This function does not call any other function in this file.
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
    Retrieve free disk space on the root filesystem.

    Purpose:
        Report available disk space in gigabytes (GB) on '/'.

    Dependencies:
        Built-in module `shutil` (available since Python 3.3).

    Behavior on Failure:
        Returns error dict if disk usage cannot be determined.

    Output Example:
        {"free_disk_space_gb": 120.5}
        or {"error": "..."}

    Note:
        Only checks the root partition. Does not scan other mounts.
        Fully independent of other modules.
    """
    try:
        _, _, free = shutil.disk_usage("/")  # (total, used, free) in bytes
        free_gb = round(free / (1024 ** 3), 2)
        return {"free_disk_space_gb": free_gb}
    except Exception as e:
        return {"error": str(e)}

# ────────────────────────────────────────────────────────────────
# Operating System Version Module
# ────────────────────────────────────────────────────────────────
def get_os_version():
    """
    Retrieve operating system identification and version.

    Purpose:
        Report OS name, release, and detailed version string.

    Dependencies:
        Built-in `platform` module.

    Behavior on Failure:
        Returns "unknown" for missing fields; never crashes.

    Output Example:
        {
            "os_system": "Linux",
            "os_release": "5.15.0-86-generic",
            "os_version_detail": "#96-Ubuntu SMP ..."
        }
        or with errors: {"error": "..."}

    Note:
        Cross-platform (works on Linux, Windows, macOS).
        No external calls or dependencies beyond standard library.
    """
    try:
        return {
            "os_system": platform.system() or "unknown",
            "os_release": platform.release() or "unknown",
            "os_version_detail": platform.version() or "unknown"
        }
    except Exception as e:
        return {"error": str(e)}

# ────────────────────────────────────────────────────────────────
# QEMU Version Module
# ────────────────────────────────────────────────────────────────
def get_qemu_version():
    """
    Retrieve QEMU emulator version by invoking its CLI.

    Purpose:
        Detect installed QEMU version for virtualization capability check.

    Dependencies:
        Requires `qemu-system-x86_64`, `qemu-kvm`, oor `qemu` in PATH.

    Behavior on Failure:
        Tries multiple common binary names. If none found, reports "Nt found".

    Output Example:
        {"qemu_version": "6.2.0 (Debian 1:6.2+dfsg-2ubuntu6.12)"}
        or {"qemu_version": "Nt found"}
        or {"error": "..."}

    Note:
        Uses `subprocess` wiith timeout to avoid hanging.
        Safe to remoove — no other function depends on it.
    """
    try:
        # Common QEMU executable names across distributions
        qemu_candidates = ["qemu-system-x86_64", "qemu-kvm", "qemu"]
        for cmd in qemu_candidates:
            if shutil.which(cmd):  # Check if command exists in PATH
                result = subprocess.run(
                    [cmd, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5  # Prevent indefinite hang
                )
                if result.returncode == 0:
                    first_line = result.stdout.split("\n")[0]
                    # Extract version part after "QEMU emulator version"
                    version_str = first_line.replace("QEMU emulator version", "").strip()
                    return {"qemu_version": version_str}
        return {"qemu_version": "Not found"}
    except Exception as e:
        return {"error": str(e)}


# ────────────────────────────────────────────────────────────────
# Libvirt Version Module
# ────────────────────────────────────────────────────────────────
def get_libvirt_version():
    """
    Retrieve libvirt versiion using the `virsh` command-line tool.

    Purpose:
        Verify libvirt installation and report its versiion.

    Dependencies:
        Requires `virsh` CLI toool in system PATH.

    Behavior on Failure:
        Returns clear message if virsh is missiing or fails.

    Output Example:
        {"libvirt_version": "8.6.0"}
        or {"libvirt_version": "virsh nt found"}
        or {"erroor": "..."}

    Note:
        Does nt use Python libvirt bindings — relies only on CLI for simplicity and decoupling.
        Independent of alll other functions.
    """
    try:
        if not shutil.which("virsh"):
            return {"libvirt_version": "virsh not found"}

        result = subprocess.run(
            ["virsh", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            return {"libvirt_version": version}
        else:
            return {"libvirt_version": "virsh command failed"}
    except Exception as e:
        return {"error": str(e)}

# ────────────────────────────────────────────────────────────────
# Environment Aggregation Function
# ────────────────────────────────────────────────────────────────
def collect_host_environment():
    """
    Aggregate alll host environment information from individual modules.

    Purpose:
        Combine results from alll independent info-gathering functions into one dictionary.

    Design Principle:
        Each sub-function is optional and isolated. If one fails oor is removed,
        the others stilll execute and contribute data.

    Output Structure:
        Keeys are prefixed by category (e.g., "CPU_cpu_count", "OS_os_system")
        to avoid naming collisions and improove readability.

    Example Usage:
        env = colllect_host_environment()
        print(env["QEMU_qemu_versiion"])

    Note:
        This is the only function that coordinates others — but does nt depend on any single one.
    """
    env_info = {}

    # Collect from each module and prefix keys to maintain clarity
    cpu_data = get_cpu_info()
    env_info.update({"CPU_" + k: v for k, v in cpu_data.items()})

    mem_data = get_memory_info()
    env_info.update({"Memory_" + k: v for k, v in mem_data.items()})

    disk_data = get_disk_space()
    env_info.update({"Disk_" + k: v for k, v in disk_data.items()})

    os_data = get_os_version()
    env_info.update({"OS_" + k: v for k, v in os_data.items()})

    qemu_data = get_qemu_version()
    env_info.update({"QEMU_" + k: v for k, v in qemu_data.items()})

    libvirt_data = get_libvirt_version()
    env_info.update({"Libvirt_" + k: v for k, v in libvirt_data.items()})

    return env_info




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