#!/bin/bash

LOG_DIR="/var/log/vmanalyzer"
LOG_FILE="$LOG_DIR/vcpu_sched_trace.log"

mkdir -p "$LOG_DIR"

log() {
    local level=$1
    local message=$2
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] [$level] $message" | tee -a "$LOG_FILE"
}

# 获取虚拟机进程 ID
get_vm_pid() {
    local vm_name=$1
    vm_pid=$(pgrep -f "qemu.*$vm_name")
    if [ -z "$vm_pid" ]; then
        log "ERROR" "Failed to find QEMU process for VM: $vm_name"
        exit 1
    fi
    echo "$vm_pid"
}

# 获取指定 vCPU 线程 ID
get_vcpu_thread() {
    local vm_pid=$1
    local vcpu_id=$2
    vcpu_thread=$(ps -L -p "$vm_pid" | grep "CPU $vcpu_id" | awk '{print $2}')
    if [ -z "$vcpu_thread" ]; then
        log "ERROR" "Failed to find vCPU thread for CPU $vcpu_id"
        exit 1
    fi
    echo "$vcpu_thread"
}

main() {
    local vm_name=$1
    local vcpu_id=$2

    if [ -z "$vm_name" ] || [ -z "$vcpu_id" ]; then
        log "ERROR" "Usage: $0 <VM_NAME> <VCPU_ID>"
        exit 1
    fi

    log "INFO" "Starting vCPU context switch trace for VM: $vm_name, vCPU: $vcpu_id"

    # 获取虚拟机 PID
    vm_pid=$(get_vm_pid "$vm_name")
    log "INFO" "VM PID: $vm_pid"

    # 获取 vCPU 线程 ID
    vcpu_thread=$(get_vcpu_thread "$vm_pid" "$vcpu_id")
    log "INFO" "vCPU Thread ID: $vcpu_thread"
}

main "$1" "$2"
