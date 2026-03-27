#!/usr/bin/env python3
"""
System patch status check tool
"""
import os
import subprocess
from datetime import datetime

def check_system_patches():
    """Check system for available security patches"""
    print("=" * 80)
    print(f"🔒 系统补丁状态检查 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Check for yum/dnf
    if os.path.exists("/usr/bin/dnf"):
        cmd = ["dnf", "check-update", "--security"]
    elif os.path.exists("/usr/bin/yum"):
        cmd = ["yum", "check-update", "--security"]
    else:
        print("❌ 不支持的包管理器")
        return
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 100:
            # Updates available
            lines = result.stdout.strip().split('\n')
            security_updates = [l for l in lines if '.x86_64' in l or '.noarch' in l]
            print(f"⚠️  发现 {len(security_updates)} 个安全补丁需要安装")
            for update in security_updates[:10]:
                print(f"   • {update.split()[0]}")
            if len(security_updates) > 10:
                print(f"   • ... 还有 {len(security_updates) - 10} 个更多")
        elif result.returncode == 0:
            print("✅ 系统已安装所有安全补丁")
    except Exception as e:
        print(f"❌ 检查失败: {e}")

if __name__ == "__main__":
    check_system_patches()
