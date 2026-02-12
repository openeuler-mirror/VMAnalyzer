#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import json
import logging
import time

try:
    from typing import Dict, List, Optional
except ImportError:
    Dict = dict
    List = list
    Optional = type(None)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
LOG_INFO = logging.info
LOG_ERROR = logging.error

class VMQgaTCPCollector:
    def __init__(self):
        self.all_vms_data = {
            "collect_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime()),
            "vm_count": 0,
            "running_vm_count": 0,
            "vms": {}
        }

    def run_virsh_cmd(self, cmd: str) -> Optional[str]:
        """执行 virsh 命令，兼容复杂引号和 JSON 格式"""
        try:
            LOG_INFO(f"执行命令：{cmd}")
            # 启用 shell=True 解析复杂命令，避免 split() 破坏 JSON 结构
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                universal_newlines=True,
                check=True,
                timeout=30  # 超时保护，避免命令卡死
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            err_msg = e.stderr.strip()
            # 过滤无关错误（如 FreeBSD 不支持某个接口）
            if "unsupported command" not in err_msg.lower() and "no such interface" not in err_msg.lower():
                LOG_ERROR(f"命令执行失败：{cmd}，错误：{err_msg}")
            return None
        except subprocess.TimeoutExpired:
            LOG_ERROR(f"命令执行超时：{cmd}（超过 30 秒）")
            return None
        except Exception as e:
            LOG_ERROR(f"命令执行异常：{cmd}，错误：{str(e)}")
            return None

    def get_all_vm_names(self) -> List[str]:
        """获取所有有效虚拟机名称（过滤空行和无效值）"""
        cmd = "virsh list --name | grep -v '^$' | grep -v '^-$'"
        output = self.run_virsh_cmd(cmd)
        return output.split() if output else []

    def get_vm_state(self, vm_name: str) -> str:
        """获取虚拟机状态（running/shut off/paused 等）"""
        cmd = f"virsh domstate {vm_name}"
        output = self.run_virsh_cmd(cmd)
        return output.strip() if output else "unknown"

    def is_vm_running(self, vm_name: str) -> bool:
        """判断虚拟机是否运行中"""
        return self.get_vm_state(vm_name) == "running"

    def call_qga_interface(self, vm_name: str, interface: str) -> Dict:
        """调用 QGA 接口，修复 JSON 格式解析问题"""
        if not self.is_vm_running(vm_name):
            LOG_INFO(f"虚拟机 {vm_name} 非运行状态，跳过 QGA 接口调用")
            return {"status": "vm_not_running", "data": {}, "error": ""}
        
        # 关键修复：用双引号包裹 JSON，内部字段用转义双引号（shell 解析无歧义）
        json_param = f'{{"execute":"{interface}"}}'
        # 外层用单引号包裹 JSON 参数，避免 shell 转义冲突
        cmd = f"virsh qemu-agent-command {vm_name} '{json_param}'"
        output = self.run_virsh_cmd(cmd)
        
        if not output:
            return {"status": "failed", "data": {}, "error": "命令无返回结果"}
        
        try:
            resp = json.loads(output)
            if "return" in resp:
                return {"status": "success", "data": resp["return"], "error": ""}
            else:
                error_msg = resp.get("error", {}).get("message", "接口返回异常")
                return {"status": "failed", "data": {}, "error": error_msg}
        except json.JSONDecodeError as e:
            LOG_ERROR(f"解析 {interface} 结果失败：{output}，错误：{str(e)}")
            return {"status": "parse_error", "data": {}, "error": str(e)}


def main():
    LOG_INFO("===== 开始执行虚拟机 QGA TCP 数据采集 =====")
    collector = VMQgaTCPCollector()
    collector.collect_all_vms()
    collector.save_to_json()
    LOG_INFO("===== 数据采集与保存完成 =====")

if __name__ == "__main__":
    main()

