#!/bin/bash
# Program:
# This program is used to check VM snapshot redundancy and snapshot chain anomaly.
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

# 日志输出
info() {
    local ts=$(date "+%Y-%m-%d %H:%M:%S")
    echo "{\"timestamp\":\"$ts\", \"status\": \"info\", \"log\": \"$1\"}" >> "$check_log"
}

error() {
    local ts=$(date "+%Y-%m-%d %H:%M:%S")
    echo "{\"timestamp\":\"$ts\", \"status\": \"error\", \"log\": \"$1\"}" >> "$check_log"
}

warn() {
    local ts=$(date "+%Y-%m-%d %H:%M:%S")
    echo "{\"timestamp\":\"$ts\", \"status\": \"warning\", \"log\": \"$1\"}" >> "$check_log"
}

# 日志文件
check_log=${virt_dir}vm_snapshot_check-$(date "+%Y-%m-%d-%H-%M-%S").log

# 快照数量阈值
SNAPSHOT_WARN_THRESHOLD=3
# 快照链深度阈值
SNAPSHOT_CHAIN_THRESHOLD=2

SNAPSHOT_EXPIRE_DAYS=7
# 检查所有虚拟机快照
check_vm_snapshot() {
    info "Checking VM snapshot redundancy and chain anomaly..."

    # 获取所有虚拟机
    VM_LIST=$(virsh list --all --name 2>/dev/null)

    for VM_NAME in $VM_LIST; do
        [ -z "$VM_NAME" ] && continue
	state=$(virsh domstate "$VM_NAME" 2>/dev/null | head -1)
        info "Checking VM: $VM_NAME (state: $state)"

        # 获取快照列表
        SNAP_LIST=$(virsh snapshot-list "$VM_NAME" 2>/dev/null)
        if [ $? -ne 0 ]; then
            error "Failed to get snapshot list for VM: $VM_NAME"
            continue
        fi

        # 统计快照数量
        SNAP_COUNT=$(echo "$SNAP_LIST" | grep -v "^-" | grep -v "Name" | wc -l)
        info "VM $VM_NAME snapshot count: $SNAP_COUNT"

        # 快照数量过多告警
        if [ "$SNAP_COUNT" -gt "$SNAPSHOT_WARN_THRESHOLD" ]; then
            warn "VM $VM_NAME has too many snapshots ($SNAP_COUNT), risk of chain explosion."
        fi

        # 空快照
        if [ "$SNAP_COUNT" -eq 0 ]; then
            info "VM $VM_NAME has no snapshot."
            continue
        fi

        get_chain_depth() {
            local vm=$1
            local snap=$2
            local depth=0
            while [ -n "$snap" ]; do
                snap=$(virsh snapshot-dumpxml "$vm" "$snap" 2>/dev/null | \
                       grep -oP '(?<=<parent>)[^<]+' | head -1)
                [ -n "$snap" ] && ((depth++))
            done
            echo $depth
        }

        # 检查快照是否异常
	if echo "$SNAP_LIST" | grep -i -E "error|invalid|broken|locked|fault|no snapshot" >/dev/null 2>&1; then
                error "VM $VM_NAME has abnormal/broken snapshot chain."
        fi

        # 检查快照链深度、过期时间及磁盘文件
        while read -r snap; do
            [ -z "$snap" ] && continue

            # 链深度检查（调用函数，见补丁2）
            chain_len=$(get_chain_depth "$VM_NAME" "$snap")
            if [ "$chain_len" -gt "$SNAPSHOT_CHAIN_THRESHOLD" ]; then
                warn "VM $VM_NAME snapshot $snap chain too deep: $chain_len levels"
            fi

            # 过期检查
            snap_time=$(virsh snapshot-dumpxml "$VM_NAME" "$snap" 2>/dev/null | grep -oP '<creationTime>\K.*(?=</creationTime>)')
            if [ -n "$snap_time" ]; then
                current_time=$(date +%s)
                expire_seconds=$((SNAPSHOT_EXPIRE_DAYS*86400))
                if [ $((current_time - snap_time)) -gt $expire_seconds ]; then
                    warn "VM $VM_NAME snapshot $snap is older than $SNAPSHOT_EXPIRE_DAYS days, please clean up"
                fi
            fi

            # 磁盘文件存在性检查
            virsh snapshot-dumpxml "$VM_NAME" "$snap" 2>/dev/null | \
                grep -oP '<source file=\x27\K[^\x27]+' | \
                while IFS= read -r d; do
                    [ -z "$d" ] && continue
                    [ ! -e "$d" ] && error "VM $VM_NAME snapshot $snap missing disk file: $d"
                done
        done < <(virsh snapshot-list "$VM_NAME" --name 2>/dev/null)
    done

    info "VM snapshot check completed."
}

# 主函数
main() {
    mk_log_dir
    echo "####################################################################################" > "$check_log"
    time=$(date +"%Y-%m-%d %H:%M:%S")
    echo "$time" >> "$check_log"

    # 执行快照检查
    check_vm_snapshot

    # 错误统计
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

# 执行
main
