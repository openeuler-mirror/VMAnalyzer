#!/bin/bash

LOG_DIR="/var/log/vmanalyzer"
LOG_FILE="$LOG_DIR/vcpu_sched_trace.log"

mkdir -p "$LOG_DIR"

log() {
    local level=$1
    local message=$2
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] [$level] $message" | tee -a "$LOG_FILE"
}

main() {
    local vm_name=$1
    local vcpu_id=$2

    if [ -z "$vm_name" ] || [ -z "$vcpu_id" ]; then
        log "ERROR" "Usage: $0 <VM_NAME> <VCPU_ID>"
        exit 1
    fi

    log "INFO" "Starting vCPU context switch trace for VM: $vm_name, vCPU: $vcpu_id"
}

main "$1" "$2"
