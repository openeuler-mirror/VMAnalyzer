#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""判断虚机是否崩溃"""
import subprocess
import json
from lxml import etree
from typing import Optional, Dict, Any
import os
import re


def execute_cmd(cmd: list, timeout: int = 30) -> Dict[str, Any]:
    """
    执行系统命令，返回标准化结果
    :param cmd: 命令列表（如 ["virsh", "domstate", "vm1"]）
    :param timeout: 超时时间
    :return: {"code": 0/非0, "stdout": 输出内容, "stderr": 错误内容}
    """
    result = {
        "code": -1,
        "stdout": "",
        "stderr": ""
    }
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout
        )
        result["code"] = proc.returncode
        result["stdout"] = proc.stdout.strip()
        result["stderr"] = proc.stderr.strip()
    except subprocess.TimeoutExpired:
        result["stderr"] = f"命令执行超时（{timeout}s）: {' '.join(cmd)}"
    except Exception as e:
        result["stderr"] = f"命令执行异常: {str(e)}"
    return result


def get_vm_list() -> list:
    """获取宿主机所有虚机名称列表"""
    cmd_result = execute_cmd(["virsh", "list", "--all", "--name"])
    if cmd_result["code"] != 0:
        return []
    return [vm for vm in cmd_result["stdout"].split("\n") if vm.strip()]


def get_vm_crash_status(vm_name: str) -> str:
    """
    检测虚机崩溃状态，采集崩溃日志
    :param vm_name: 虚机名称
    :return: JSON格式结果
    """
    result = {
        "vm_name": vm_name,
        "crashed": False,
        "crash_reason": "",
        "crash_log_snippet": "",
        "success": False,
        "error": ""
    }

    # 1. 检查Libvirt状态
    state_cmd = ["virsh", "domstate", vm_name]
    state_result = execute_cmd(state_cmd)
    if state_result["code"] == 0 and state_result["stdout"].lower() == "crashed":
        result["crashed"] = True
        result["crash_reason"] = "Libvirt标记为崩溃状态"

    # 2. 检查QEMU日志（/var/log/libvirt/qemu/<vm-name>.log）
    log_path = f"/var/log/libvirt/qemu/{vm_name}.log"
    if os.path.exists(log_path):
        try:
            # 读取最后100行日志
            with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()[-100:]  # 取最后100行

            # 匹配崩溃关键字
            crash_patterns = [
                r"kernel panic",
                r"qemu: fatal error",
                r"crash",
                r"abort",
                r"segmentation fault",
                r"core dumped"
            ]
            crash_lines = []
            for line in lines:
                if any(re.search(p, line, re.I) for p in crash_patterns):
                    crash_lines.append(line.strip())
                    result["crashed"] = True

            # 提取崩溃日志片段
            if crash_lines:
                result["crash_log_snippet"] = "\n".join(crash_lines[-10:])  # 最后10行崩溃日志
                if not result["crash_reason"]:
                    result["crash_reason"] = "日志中检测到崩溃关键字"

        except Exception as e:
            result["error"] = f"读取日志失败: {str(e)}"

    # 3. 检查虚机进程是否异常
    ps_cmd = ["ps", "-ef"]
    ps_result = execute_cmd(ps_cmd)
    if ps_result["code"] == 0:
        qemu_pattern = re.compile(rf"guest={vm_name}.*\s", re.I)
        if not any(qemu_pattern.search(line) for line in ps_result["stdout"].split("\n")):
            # 无QEMU进程但状态非关机
            if result["crashed"] is False and state_result["stdout"].lower() != "shut off":
                result["crashed"] = True
                result["crash_reason"] = "QEMU进程已退出但虚机状态非关机"

    result["success"] = True
    return json.dumps(result, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    import sys
    vms = get_vm_list()
    if not vms:
        print(json.dumps({"error": "没有找到任何虚机或执行virsh命令失败"}, ensure_ascii=False, indent=2))
        sys.exit(1)

    results = []
    for vm in vms:
        # 调用已有的获取XML函数，它返回JSON字符串，我们需要解析为字典
        vm_result_json = get_vm_crash_status(vm)
        vm_result = json.loads(vm_result_json)
        results.append(vm_result)

    # 输出所有虚机的结果（JSON数组）
    print(json.dumps(results, ensure_ascii=False, indent=2))
