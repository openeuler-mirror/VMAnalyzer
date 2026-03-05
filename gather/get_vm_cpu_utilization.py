#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import json
import logging
import time
import argparse
import os
from datetime import datetime

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

class VMCollector:
    def __init__(self, output_dir: str = "./get_vm_cpu_utilization_data", cmd_timeout: int = 30):
        self.output_dir = output_dir
        self.cmd_timeout = cmd_timeout
        try:
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)
        except Exception as e:
            LOG_ERROR(f"创建输出目录失败：{self.output_dir}，错误：{str(e)}")
            raise SystemExit(1)

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
                text=True,
                check=True,
                timeout=self.cmd_timeout  # 超时保护，避免命令卡死
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            err_msg = e.stderr.strip()
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
        """获取虚拟机状态（running/shut off等）"""
        cmd = f"virsh domstate {vm_name}"
        output = self.run_virsh_cmd(cmd)
        return output.strip() if output else "unknown"

    def call_qga_interface(self, vm_name: str, interface: str) -> Dict:
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

    def collect_single_vm_data(self, vm_name: str) -> Dict:
        LOG_INFO(f"\n===== 开始采集虚拟机：{vm_name} =====")
        
        cpu_utilization = self.call_qga_interface(vm_name, "guest-get-cpu-utilization")
        vm_data = {
            "name": vm_name,
            "get_cpu_utilization": {
                "interface": "guest-get-cpu-utilization",
                "error": cpu_utilization["error"],
                "data": cpu_utilization["data"]
            },
        }
        LOG_INFO(f"===== 虚拟机 {vm_name} 采集完成 =====")
        return vm_data

    def collect_all_vms(self):
        """采集所有虚拟机数据"""
        vm_names = self.get_all_vm_names()
        if not vm_names:
            LOG_ERROR("未找到任何虚拟机")
            return
        
        self.all_vms_data["vm_count"] = len(vm_names)
        # 统计运行中的虚拟机数量
        running_vms = [name for name in vm_names]
        self.all_vms_data["running_vm_count"] = len(running_vms)
        
        LOG_INFO(f"共找到 {len(vm_names)} 台虚拟机，其中 {len(running_vms)} 台运行中：{running_vms}")

        for vm_name in vm_names:
            vm_data = self.collect_single_vm_data(vm_name)
            self.all_vms_data["vms"][vm_name] = vm_data

    def save_data(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"get_cpu_utilization_{timestamp}.json"
        file_path = os.path.join(self.output_dir, file_name)

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.all_vms_data, f, indent=2, ensure_ascii=False)
            LOG_INFO(f"采集数据已保存到：{file_path}")
        except Exception as e:
            LOG_ERROR(f"保存数据失败：{str(e)}")

def parse_args():
    """改动8：补充argparse参数解析，支持命令行配置"""
    parser = argparse.ArgumentParser(description="采集KVM虚拟机CPU利用率数据")
    parser.add_argument(
        "-o", "--output-dir",
        default="./get_vm_cpu_utilization_data",
        help="数据输出目录（默认：./get_vm_cpu_utilization_data）"
    )
    parser.add_argument(
        "-t", "--timeout",
        type=int,
        default=30,
        help="virsh命令超时时间（秒，默认：30）"
    )
    return parser.parse_args()

def main():
    LOG_INFO("===== 开始进行虚拟机数据采集 =====")
    collector = VMCollector()
    collector.collect_all_vms()
    collector.save_data()
    LOG_INFO("===== 数据采集与保存完成 =====")

if __name__ == "__main__":
    main()

