#!/bin/bash
# Program:
# Trace and analyze scheduling events for a specific vCPU thread.
# History:
# Dinglimin Create the file.

# 日志文件
LOG_DIR="/var/log/vmanalyzer"
LOG_FILE="$LOG_DIR/vcpu_sched_trace.log"

# 创建日志目录
mkdir -p "$LOG_DIR"

# 日志函数
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

# 跟踪上下文切换事件
trace_sched_switch() {
    local vcpu_thread=$1
    log "INFO" "Tracing context switch events for vCPU thread: $vcpu_thread"
    perf trace -e sched:sched_switch -T -p "$vcpu_thread" -o "$LOG_FILE.tmp" &
    PERF_PID=$!
    sleep 10
    sudo kill -SIGINT $PERF_PID
    if [ $? -ne 0 ]; then
        log "ERROR" "Failed to kill perf"
        exit 1
    fi
}

# 分析上下文切换事件
analyze_sched_switch() {
    log "INFO" "Analyzing context switch events"

    # 统计上下文切换总数
    total_switches=$(grep "sched:sched_switch" "$LOG_FILE.tmp" | wc -l)
    log "INFO" "Total context switches: $total_switches"
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

    # 跟踪上下文切换事件
    trace_sched_switch "$vcpu_thread"

    # 分析上下文切换事件
    analyze_sched_switch

    # 清理临时文件
    rm -f "$LOG_FILE.tmp"

    log "INFO" "Analysis completed. See report in: $LOG_FILE"
}

# 执行主函数
if [ $# -lt 2 ]; then
    echo "Usage: $0 <VM_NAME> <VCPU_ID>"
    exit 1
fi

main "$1" "$2"
