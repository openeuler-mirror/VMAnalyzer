#!/usr/bin/env python3
# coding: utf-8
"""
Real-time VM monitoring top mode
"""
import time
import json
import redis
import os

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

def vm_top():
    """Display real-time VM metrics in top-like format"""
    r = redis.Redis()
    
    try:
        while True:
            clear_screen()
            print("=" * 100)
            print(f"VM Top - 实时监控 | 按 Ctrl+C 退出 | {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 100)
            print(f"{'VM UUID':<40} {'CPU%':<6} {'MEM%':<6} {'DISK%':<6} {'STATUS'}")
            print("-" * 100)
            
            keys = r.keys("vm:*")
            for key in keys:
                raw = r.get(key)
                if raw is None:
                    continue
                data = json.loads(raw)
                status = "Operation message" if data.get("status") == "running" else "Operation message"
                print(f"{key.decode():<40} "
                      f"{data.get('cpu_usage', 0):<6.1f} "
                      f"{data.get('memory_usage', 0):<6.1f} "
                      f"{data.get('disk_usage', 0):<6.1f} "
                      f"{status}")
            
            time.sleep(2)
    except KeyboardInterrupt:
        print("Operation message")

if __name__ == "__main__":
    vm_top()
