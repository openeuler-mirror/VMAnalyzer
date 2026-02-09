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

# 运行 perf stat 采集调度事件
run_perf_stat() {
    local vm_pid=$1
    log "INFO" "Collecting vCPU scheduling events for PID: $vm_pid"
    perf stat -e sched:sched_stat_sleep \
              -e sched:sched_stat_iowait \
              -e sched:sched_stat_blocked \
              -e sched:sched_switch \
              -e sched:sched_migrate_task \
              -e sched:sched_wakeup \
              -e sched:sched_wait_task \
              -p "$vm_pid" -o "$LOG_FILE.tmp" sleep 10
    if [ $? -ne 0 ]; then
        log "ERROR" "Failed to collect perf data"
        exit 1
    fi
}

# 解析 perf 结果并生成报告
parse_perf_results() {
    local total_events=0
    local sleep_events=0
    local iowait_events=0
    local blocked_events=0

    # 提取事件计数
    sleep_events=$(grep "sched:sched_stat_sleep" "$LOG_FILE.tmp" | awk '{print $1}' | tr -d ',')
    iowait_events=$(grep "sched:sched_stat_iowait" "$LOG_FILE.tmp" | awk '{print $1}' | tr -d ',')
    blocked_events=$(grep "sched:sched_stat_blocked" "$LOG_FILE.tmp" | awk '{print $1}' | tr -d ',')

    # 计算总事件数
    total_events=$((sleep_events + iowait_events + blocked_events + switch_events + migrate_events + wakeup_events + wait_events))

    # 计算占比
    sleep_percent=$(echo "scale=2; $sleep_events*100/$total_events" | bc)
    iowait_percent=$(echo "scale=2; $iowait_events*100/$total_events" | bc)
    blocked_percent=$(echo "scale=2; $blocked_events*100/$total_events" | bc)

    # 生成报告
    echo "----------------------------------------" | tee -a "$LOG_FILE"
    echo "vCPU Scheduling Latency Analysis Report" | tee -a "$LOG_FILE"
    echo "----------------------------------------" | tee -a "$LOG_FILE"
    printf "%-30s %-10s %-10s\n" "Event" "Count" "Percentage" | tee -a "$LOG_FILE"
    printf "%-30s %-10s %-10s\n" "sched_stat_sleep" "$sleep_events" "$(printf "%0.2f%%" "$sleep_percent")" | tee -a "$LOG_FILE"
    printf "%-30s %-10s %-10s\n" "sched_stat_iowait" "$iowait_events" "$(printf "%0.2f%%" "$iowait_percent")" | tee -a "$LOG_FILE"
    printf "%-30s %-10s %-10s\n" "sched_stat_blocked" "$blocked_events" "$(printf "%0.2f%%" "$blocked_percent")" | tee -a "$LOG_FILE"
    echo "----------------------------------------" | tee -a "$LOG_FILE"
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

    # 运行 perf stat
    run_perf_stat "$vm_pid"

    # 解析结果
    parse_perf_results
}

main "$@"
