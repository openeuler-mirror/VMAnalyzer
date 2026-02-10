#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import json
import logging
import time
import argparse
import os
from datetime import datetime
from typing import Dict, List, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


class VMMemTopNCollector:
    def __init__(self, top_n: int = 5, poll_interval: int = 60, output_dir: str = "./vm_mem_topn_data"):
        self.top_n = top_n
        self.poll_interval = poll_interval
        self.output_dir = output_dir
        self._init_output_dir()

        self.collect_data = {
            "collect_time": "",
            "running_vm_count": 0,
            "vm_list": {}
        }

    def _init_output_dir(self) -> None:
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)

    def _exec_virsh_cmd(self, cmd: str) -> Optional[str]:
        try:
            logger.info(f"执行命令：{cmd}")
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                universal_newlines=True,
                check=True,
                timeout=30
            )
            output = result.stdout.strip()
            return output if output else None

        except subprocess.CalledProcessError as e:
            err_msg = e.stderr.strip()
            logger.error(f"命令执行失败：{cmd}，错误：{err_msg}")
            return None

        except subprocess.TimeoutExpired:
            logger.error(f"命令执行超时：{cmd}（超过30秒）")
            return None

        except Exception as e:
            logger.error(f"命令执行异常：{cmd}，错误：{str(e)}")
            return None

    def get_running_vms(self) -> List[str]:
        cmd = "virsh list --name | grep -v '^$'"
        output = self._exec_virsh_cmd(cmd)
        return output.split() if output else []

    def get_vm_mem_topn(self, vm_name: str) -> Optional[List[Dict]]:
        qga_params = {
            "execute": "guest-get-memtopn-status",
            "arguments": {"memtopn-num": str(self.top_n)}
        }
        qga_cmd = f"virsh qemu-agent-command {vm_name} '{json.dumps(qga_params)}'"
        output = self._exec_virsh_cmd(qga_cmd)

        if not output:
            logger.error(f"VM {vm_name} 内存TopN信息采集失败：无返回数据")
            return None

        try:
            resp = json.loads(output)
            if "return" not in resp:
                logger.error(f"VM {vm_name} QGA返回格式异常：{output}")
                return None
            return resp["return"]

        except json.JSONDecodeError as e:
            logger.error(f"VM {vm_name} QGA返回解析失败：{str(e)}，原始数据：{output}")
            return None

    def format_process_data(self, process_data: List[Dict]) -> List[Dict]:
        formatted_list = []
        for process in process_data:
            proc_id = process.get("process-id", "未知").strip()
            proc_info = process.get("process-info", {})
            
            # 兼容返回值中嵌套process-info的异常格式
            if "process-info" in proc_info:
                proc_info = proc_info["process-info"]

            formatted_item = {
                "process_id": proc_id,
                "user": proc_info.get("user", "未知").strip(),
                "cpu_util": proc_info.get("cpu-util", "0").strip(),
                "mem_util": proc_info.get("mem-util", "0").strip(),
                "open_files": proc_info.get("open-files", "N/A").strip(),
                "cmd_name": proc_info.get("cmd-name", "未知").strip().replace("\n", "")
            }
            formatted_list.append(formatted_item)

        return formatted_list

    def collect_all_vms_data(self) -> None:
        self.collect_data["collect_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        running_vms = self.get_running_vms()
        self.collect_data["running_vm_count"] = len(running_vms)

        if not running_vms:
            logger.info("当前无运行中的虚拟机")
            self.collect_data["vm_list"] = {}
            return

        for vm_name in running_vms:
            logger.info(f"\n===== 开始采集VM {vm_name} 内存Top{self.top_n} 进程信息 =====")
            raw_data = self.get_vm_mem_topn(vm_name)

            if not raw_data:
                self.collect_data["vm_list"][vm_name] = {
                    "status": "采集失败",
                    "process_list": []
                }
                continue

            formatted_data = self.format_process_data(raw_data)
            self.collect_data["vm_list"][vm_name] = {
                "status": "采集成功",
                "process_list": formatted_data,
                "top_n": self.top_n
            }
            logger.info(f"VM {vm_name} 采集完成，共获取 {len(formatted_data)} 个进程信息")

    def save_collect_data(self) -> None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"vm_mem_topn_{timestamp}.json"
        file_path = os.path.join(self.output_dir, file_name)

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.collect_data, f, indent=2, ensure_ascii=False)
            logger.info(f"采集数据已保存到：{file_path}")

        except Exception as e:
            logger.error(f"保存数据失败：{str(e)}")

    def start_polling(self) -> None:
        logger.info("===== 启动内存TopN进程信息轮询采集 =====")
        logger.info(f"轮询间隔：{self.poll_interval} 秒 | TopN值：{self.top_n} | 输出目录：{self.output_dir}")
        logger.info("按 Ctrl+C 停止采集\n")

        try:
            while True:
                self.collect_all_vms_data()
                self.save_collect_data()
                logger.info(f"\n等待 {self.poll_interval} 秒后开始下一次采集...\n")
                time.sleep(self.poll_interval)

        except KeyboardInterrupt:
            logger.info("\n===== 用户终止采集，程序退出 =====")

        except Exception as e:
            logger.error(f"轮询采集异常：{str(e)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="VM 内存TopN进程信息采集脚本")
    parser.add_argument("--top-n", type=int, default=5, help="内存TopN的N值，默认5")
    parser.add_argument("--poll-interval", type=int, default=60, help="轮询间隔（秒），默认60")
    parser.add_argument("--output-dir", type=str, default="./vm_mem_topn_data", help="数据输出目录")
    return parser.parse_args()


if __name__ == "__main__":
    try:
        from typing import Dict, List, Optional
    except ImportError:
        pass

    main()

