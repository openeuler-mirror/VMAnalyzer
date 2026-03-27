#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取虚拟机 vCPU 实际生效的 CPU flags
通过 guest-agent 读取 /proc/cpuinfo 中的 flags 行
"""

import subprocess
import json
import logging
import argparse
import os
import time
from typing import Dict, List, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
LOG_INFO = logging.info
LOG_ERROR = logging.error


def run_virsh_cmd(cmd: str) -> Optional[str]:
    """执行 virsh 命令并返回标准输出"""
    try:
        LOG_INFO(f"执行命令：{cmd}")
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            universal_newlines=True,
            timeout=30
        )
        if result.returncode != 0:
            LOG_ERROR(f"命令失败：{result.stderr.strip()}")
            return None
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        LOG_ERROR("命令执行超时")
        return None
    except Exception as e:
        LOG_ERROR(f"执行命令异常：{e}")
        return None


def get_domain_uuid(vm_name: str) -> Optional[str]:
    """通过 virsh 获取虚拟机 UUID"""
    cmd = f"virsh domuuid {vm_name}"
    uuid = run_virsh_cmd(cmd)
    if not uuid:
        LOG_ERROR(f"无法获取虚拟机 {vm_name} 的 UUID")
    return uuid


def get_vm_cpu_flags_via_qga(vm_name: str) -> Optional[List[str]]:
    """
    使用 QEMU Guest Agent 读取 /proc/cpuinfo 中的 flags
    返回 flags 列表
    """
    # 构造 guest-exec 命令读取 /proc/cpuinfo
    qga_cmd = {
        "execute": "guest-exec",
        "arguments": {
            "path": "/bin/sh",
            "arg": ["-c", "grep '^flags' /proc/cpuinfo | head -1"],
            "capture-output": True
        }
    }
    cmd_str = json.dumps(qga_cmd, separators=(',', ':'))
    virsh_cmd = f'virsh qemu-agent-command {vm_name} \'{cmd_str}\' --timeout 30'
    output = run_virsh_cmd(virsh_cmd)
    if not output:
        return None

    try:
        # 解析 guest-exec 返回的 JSON
        resp = json.loads(output)
        pid = resp.get("return", {}).get("pid")
        if not pid:
            LOG_ERROR("guest-exec 未返回 pid")
            return None

        # 等待进程结束并获取输出
        time.sleep(0.5)
        status_cmd = {
            "execute": "guest-exec-status",
            "arguments": {"pid": pid}
        }
        status_cmd_str = json.dumps(status_cmd, separators=(',', ':'))
        status_virsh_cmd = f'virsh qemu-agent-command {vm_name} \'{status_cmd_str}\' --timeout 30'
        status_output = run_virsh_cmd(status_virsh_cmd)
        if not status_output:
            return None

        status_resp = json.loads(status_output)
        status_ret = status_resp.get("return", {})
        if not status_ret.get("exited"):
            LOG_ERROR("guest-exec 进程未结束")
            return None

        out_data = status_ret.get("out-data", "")
        if not out_data:
            LOG_ERROR("guest-exec 无输出数据")
            return None

        # base64 解码输出
        import base64
        cpuinfo_line = base64.b64decode(out_data).decode("utf-8").strip()
        # 提取 flags 字段
        parts = cpuinfo_line.split(":", 1)
        if len(parts) != 2:
            LOG_ERROR("无法解析 cpuinfo flags 行")
            return None
        flags_str = parts[1].strip()
        flags = flags_str.split()
        return flags
    except Exception as e:
        LOG_ERROR(f"解析 guest-agent 返回失败：{e}")
        return None


def get_vm_cpu_flags(vm_name: str) -> Dict:
    """主入口：返回单台 VM 的 CPU flags 信息"""
    uuid = get_domain_uuid(vm_name)
    if not uuid:
        return {}
    flags = get_vm_cpu_flags_via_qga(vm_name)
    if flags is None:
        return {}
    return {
        "vm_name": vm_name,
        "uuid": uuid,
        "cpu_flags": flags,
        "flags_count": len(flags),
        "timestamp": int(time.time())
    }


def main():
    parser = argparse.ArgumentParser(description="获取虚拟机 vCPU 实际生效的 CPU flags")
    parser.add_argument("vm_name", help="虚拟机名称")
    parser.add_argument("-o", "--output", help="可选：输出 JSON 文件路径")
    args = parser.parse_args()

    info = get_vm_cpu_flags(args.vm_name)
    if not info:
        LOG_ERROR("无法获取信息，请确认虚拟机存在、已运行且 QEMU Guest Agent 可用")
        return

    print(json.dumps(info, indent=2, ensure_ascii=False))

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(info, f, indent=2, ensure_ascii=False)
        LOG_INFO(f"结果已写入 {args.output}")


if __name__ == "__main__":
    main()
