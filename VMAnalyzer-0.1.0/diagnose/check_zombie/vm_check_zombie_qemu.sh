#!/bin/bash
# Program:
# This program is used to check zombie/orphan QEMU processes.
# History:
# Dinglimin Create the file.

# 日志目录
virt_dir=/var/log/vmanalyzer/

# 日志目录创建
mk_log_dir() {
    if [ ! -d "$virt_dir" ]; then
        mkdir -p "$virt_dir"
    fi
}

# 日志输出（和check_secret、快照脚本完全一致的JSON格式）
info() {
    echo "{\"status\": \"info\", \"log\": \"$1\"}" >> "$check_log"
}

error() {
    echo "{\"status\": \"error\", \"log\": \"$1\"}" >> "$check_log"
}

warn() {
    echo "{\"status\": \"warning\", \"log\": \"$1\"}" >> "$check_log"
}

# 日志文件（命名规范对齐）
check_log=${virt_dir}vm_zombie_qemu_check-$(date "+%Y-%m-%d-%H-%M-%S").log

# 检查QEMU僵尸/孤儿进程
check_zombie_qemu() {
    info "Checking zombie/orphan QEMU processes..."

    # 获取所有运行中虚拟机名称（用于校验QEMU进程合法性）
    RUNNING_VMS=$(virsh list --name 2>/dev/null)

    # 获取所有QEMU进程（过滤grep自身）
    QEMU_PROCESSES=$(ps aux | grep -E "qemu-kvm|qemu-system" | grep -v grep)

    if [ -z "$QEMU_PROCESSES" ]; then
        info "No QEMU processes found."
        return 0
    fi

    # 遍历QEMU进程，校验是否为合法虚拟机对应的进程
    echo "$QEMU_PROCESSES" | while read -r PROC_LINE; do
        PID=$(echo "$PROC_LINE" | awk '{print $2}')
        PROC_CMD=$(echo "$PROC_LINE" | awk '{print $0}')

        # 判断进程是否为僵尸进程（状态为Z）
        PROC_STATUS=$(ps -p "$PID" -o stat= 2>/dev/null | grep -q "Z")
        if [ $? -eq 0 ]; then
            error "Found zombie QEMU process: PID=$PID, Command=$PROC_CMD"
            continue
        fi

        # 判断进程是否为孤儿进程（无对应运行中虚拟机）
        VM_NAME=$(echo "$PROC_CMD" | grep -oE "--name\s+[a-zA-Z0-9_-]+" | awk '{print $2}')
        if [ -z "$VM_NAME" ]; then
            warn "Found QEMU process with no VM name: PID=$PID, Command=$PROC_CMD"
            continue
        fi

        # 校验VM是否在运行中，不存在则为孤儿进程
        if ! echo "$RUNNING_VMS" | grep -q "$VM_NAME"; then
            error "Found orphan QEMU process (no running VM): PID=$PID, VM=$VM_NAME, Command=$PROC_CMD"
        else
            info "Valid QEMU process: PID=$PID, VM=$VM_NAME"
        fi
    done

    info "Zombie/orphan QEMU process check completed."
}

# 主函数（结构和其他脚本完全对齐）
main() {
    mk_log_dir
    echo "####################################################################################" > "$check_log"
    time=$(date +"%Y-%m-%d %H:%M:%S")
    echo "$time" >> "$check_log"

    # 执行QEMU进程检查
    check_zombie_qemu

    # 错误统计（和快照脚本一致，包含error和warn）
    ERROR_COUNT=$(grep -c '"status": "error"' "$check_log")
    WARN_COUNT=$(grep -c '"status": "warning"' "$check_log")

    if [ "$ERROR_COUNT" -gt 0 ] || [ "$WARN_COUNT" -gt 0 ]; then
        echo "Check completed with $ERROR_COUNT error(s) and $WARN_COUNT warning(s). Log: $check_log"
        exit 1
    else
        echo "Check completed successfully. No errors found."
        exit 0
    fi
}

# 执行主函数
main
