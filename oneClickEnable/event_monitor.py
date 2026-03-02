#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of
# the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details._
import os
import sys
import time
import subprocess
import logging
import signal
import atexit

LOG_FILE = "/var/log/virsh_events.log"
RAW_LOG_FILE = "/var/log/virsh_events_raw.log"
PID_FILE = "/var/run/virsh_event_monitor.pid"
ALERT_SCRIPT = "/path/to/alert_script.sh"
CHECK_INTERVAL = 1
VIRSH_WAIT_TIMEOUT = 5

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
os.makedirs(os.path.dirname(RAW_LOG_FILE), exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger()

EXCEPTION_EVENTS = [
    "watchdog",
    "io-error",
    "control-error",
    "device-removal-failed",
    "block-threshold",
    "memory-failure",
    "crashed",
    "destroyed",
    "suspended",
    "failed",
    "canceled"
]

def check_running():
    if os.path.exists(PID_FILE):
        with open(PID_FILE, "r") as f:
            pid = f.read().strip()
        try:
            os.kill(int(pid), 0)
            logger.error(f"脚本已在运行，PID: {pid}")
            print(f"脚本已在运行，PID: {pid}")
            sys.exit(1)
        except OSError:
            logger.warning("发现旧的PID文件，已删除")
            os.remove(PID_FILE)

def cleanup():
    logger.info("脚本正在退出，清理资源...")
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)
    if "virsh_process" in globals() and virsh_process.poll() is None:
        virsh_process.terminate()
        try:
            virsh_process.wait(timeout=VIRSH_WAIT_TIMEOUT)
        except subprocess.TimeoutExpired:
            virsh_process.kill()

signal.signal(signal.SIGINT, lambda sig, frame: cleanup() or sys.exit(0))
signal.signal(signal.SIGTERM, lambda sig, frame: cleanup() or sys.exit(0))
atexit.register(cleanup)

def check_exceptions(event_line):
    for exception in EXCEPTION_EVENTS:
        if exception.lower() in event_line.lower():
            logger.error(f"检测到异常事件：{exception}")
            logger.error(f"事件详情：{event_line}")

            if ALERT_SCRIPT and os.path.exists(ALERT_SCRIPT):
                try:
                    subprocess.run([ALERT_SCRIPT, event_line], check=True)
                except subprocess.CalledProcessError as e:
                    logger.error(f"执行告警脚本失败：{e}")
            return True
    return False

def main():
    check_running()
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))
    logger.info("启动 virsh 事件监控")

    open(RAW_LOG_FILE, "w").close()
    virsh_cmd = ["stdbuf", "-oL", "-eL", "virsh", "event", "--all", "--loop", "--timestamp"]
    global virsh_process
    virsh_process = subprocess.Popen(
        virsh_cmd,
        stdout=open(RAW_LOG_FILE, "a"),
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    logger.info(f"virsh event 命令已启动，PID: {virsh_process.pid}")
    logger.info(f"原始日志文件: {RAW_LOG_FILE}")
    logger.info(f"分析日志文件: {LOG_FILE}")
    logger.info("开始监控日志文件变化...")
    last_size = os.path.getsize(RAW_LOG_FILE)
    while True:
        if virsh_process.poll() is not None:
            logger.error("virsh event 命令已退出，正在重启...")
            print("virsh event 命令已退出，正在重启...")
            virsh_process = subprocess.Popen(
                virsh_cmd,
                stdout=open(RAW_LOG_FILE, "a"),
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            logger.info(f"virsh event 命令已重启，新PID: {virsh_process.pid}")

            last_size = os.path.getsize(RAW_LOG_FILE)
        current_size = os.path.getsize(RAW_LOG_FILE)
        if current_size > last_size:
            with open(RAW_LOG_FILE, "r") as f:
                f.seek(last_size)
                new_content = f.read()
            for line in new_content.strip().split("\n"):
                if line:
                    check_exceptions(line)
            last_size = current_size
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()

