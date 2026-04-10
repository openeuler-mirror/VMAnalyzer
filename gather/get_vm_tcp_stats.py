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
        try:
            LOG_INFO(f"执行命令：{cmd}")
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                universal_newlines=True,
                check=True,
                timeout=30
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            err_msg = e.stderr.strip()
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
        cmd = "virsh list --name | grep -v '^$' | grep -v '^-$'"
        output = self.run_virsh_cmd(cmd)
        return output.split() if output else []

    def get_vm_state(self, vm_name: str) -> str:
        cmd = f"virsh domstate {vm_name}"
        output = self.run_virsh_cmd(cmd)
        return output.strip() if output else "unknown"

    def is_vm_running(self, vm_name: str) -> bool:
        return self.get_vm_state(vm_name) == "running"

    def call_qga_interface(self, vm_name: str, interface: str) -> Dict:
        if not self.is_vm_running(vm_name):
            LOG_INFO(f"虚拟机 {vm_name} 非运行状态，跳过 QGA 接口调用")
            return {"status": "vm_not_running", "data": {}, "error": ""}
        
        json_param = f'{{"execute":"{interface}"}}'
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

    def calculate_tcp_retrans_rate(self, tcp_snmp_data: Dict) -> Optional[float]:
        try:
            retranssegs = int(tcp_snmp_data.get("retranssegs", 0))
            outsegs = int(tcp_snmp_data.get("outsegs", 0))
            if outsegs == 0:
                LOG_INFO("TCP 发送总数为 0，重传率设为 0.0")
                return 0.0
            retrans_rate = (retranssegs / outsegs) * 100
            return round(retrans_rate, 4)
        except (ValueError, ZeroDivisionError) as e:
            LOG_ERROR(f"计算 TCP 重传率失败：{str(e)}")
            return None

    def collect_single_vm_tcp_data(self, vm_name: str) -> Dict:
        LOG_INFO(f"\n===== 开始采集虚拟机：{vm_name} =====")
        try:
            vm_state = self.get_vm_state(vm_name)
            is_running = self.is_vm_running(vm_name)
        
            tcp_snmp = self.call_qga_interface(vm_name, "bc-guest-get-tcp-snmp") if is_running else {"status": "vm_not_running", "data": {}, "error": ""}
            tcp_retrans_rate = self.calculate_tcp_retrans_rate(tcp_snmp["data"]) if tcp_snmp["status"] == "success" else None
        
            tcp_conn_state = self.call_qga_interface(vm_name, "guest-get-tcp-conn-state") if is_running else {"status": "vm_not_running", "data": {}, "error": ""}
            tcp_conn = self.call_qga_interface(vm_name, "guest-get-tcp-conn") if is_running else {"status": "vm_not_running", "data": {}, "error": ""}

            vm_data = {
                "name": vm_name,
                "state": vm_state,
                "tcp_retrans_data": {
                    "interface": "bc-guest-get-tcp-snmp",
                    "status": tcp_snmp["status"],
                    "error": tcp_snmp["error"],
                    "data": tcp_snmp["data"],
                    "tcp_retrans_rate_percent": tcp_retrans_rate
                },
                "tcp_conn_state": {
                    "interface": "guest-get-tcp-conn-state",
                    "status": tcp_conn_state["status"],
                    "error": tcp_conn_state["error"],
                    "data": tcp_conn_state["data"]
                },
                "tcp_conn": {
                    "interface": "guest-get-tcp-conn",
                    "status": tcp_conn["status"],
                    "error": tcp_conn["error"],
                    "data": tcp_conn["data"]
                }
            }
            LOG_INFO(f"===== 虚拟机 {vm_name} 采集完成 =====")
            return vm_data
        except Exception as e:
            LOG_ERROR(f"采集虚拟机 {vm_name} 数据失败：{str(e)}")
            return {
                "name": vm_name,
                "state": "collect_failed",
                "tcp_retrans_data": {"status": "collect_failed", "error": str(e), "data": {}, "tcp_retrans_rate_percent": 0.0},
                "tcp_conn_state": {"status": "collect_failed", "error": str(e), "data": {}},
                "tcp_conn": {"status": "collect_failed", "error": str(e), "data": {}}
            }

    def collect_all_vms(self):
        vm_names = self.get_all_vm_names()
        if not vm_names:
            LOG_ERROR("未找到任何虚拟机")
            return
        
        self.all_vms_data["vm_count"] = len(vm_names)
        running_vms = [name for name in vm_names if self.is_vm_running(name)]
        self.all_vms_data["running_vm_count"] = len(running_vms)
        
        LOG_INFO(f"共找到 {len(vm_names)} 台虚拟机，其中 {len(running_vms)} 台运行中：{running_vms}")

        for vm_name in vm_names:
            vm_data = self.collect_single_vm_tcp_data(vm_name)
            self.all_vms_data["vms"][vm_name] = vm_data

    def save_to_json(self, file_path: Optional[str] = None):
        if not file_path:
            file_path = f"vm_qga_tcp_stats_{int(time.time())}.json"
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.all_vms_data, f, indent=2, ensure_ascii=False)
            LOG_INFO(f"\n所有虚拟机 TCP 数据已保存到：{file_path}")
        except Exception as e:
            LOG_ERROR(f"保存 JSON 文件失败：{str(e)}")

def main():
    LOG_INFO("===== 开始执行虚拟机 QGA TCP 数据采集 =====")
    collector = VMQgaTCPCollector()
    collector.collect_all_vms()
    collector.save_to_json()
    LOG_INFO("===== 数据采集与保存完成 =====")

if __name__ == "__main__":
    main()

