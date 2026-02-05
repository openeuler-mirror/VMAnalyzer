#!/bin/bash
# Program:
# Advanced analysis of vCPU scheduling latency using perf stat.
# History:
# Dinglimin Create the file.

LOG_DIR="/var/log/vmanalyzer"
LOG_FILE="$LOG_DIR/vcpu_sched_latency-$(date +%Y%m%d%H%M%S).log"

mkdir -p "$LOG_DIR"

log() {
    local level=$1
    local message=$2
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] [$level] $message" | tee -a "$LOG_FILE"
}

get_vm_pid() {
    local vm_name=$1
    vm_pid=$(pgrep -f "qemu.*$vm_name")
    if [ -z "$vm_pid" ]; then
        log "ERROR" "Failed to find QEMU process for VM: $vm_name"
        exit 1
    fi
    echo "$vm_pid"
}

main() {
    local vm_name=$1
    if [ -z "$vm_name" ]; then
        log "ERROR" "Usage: $0 <VM_NAME>"
        exit 1
    fi
    log "INFO" "Starting advanced vCPU scheduling analysis for VM: $vm_name"
    vm_pid=$(get_vm_pid "$vm_name")
    log "INFO" "VM PID: $vm_pid"
}

main "$@"
