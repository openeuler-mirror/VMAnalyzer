#!/usr/bin/env python3
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

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
os.makedirs(os.path.dirname(RAW_LOG_FILE), exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
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
        with open(PID_FILE, 'r') as f:
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
    if 'virsh_process' in globals() and virsh_process.poll() is None:
        virsh_process.terminate()
        try:
            virsh_process.wait(timeout=5)
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

if __name__ == "__main__":
    main()

