#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_command() {
    if ! command -v $1 &> /dev/null; then
        log_error "命令 $1 未找到，请安装相关软件包"
        exit 1
    fi
}

check_source_to_target_network() {
    local src_host=$1
    local dst_host=$2
    
    log_info "检查源主机 $src_host 与目标主机 $dst_host 网络连通性..."
    
    local result=$(ssh $src_host "ping -c 3 -W 5 $dst_host &> /dev/null; echo \$?")
    
    if [ "$result" -eq 0 ]; then
        log_info "网络连通性检查通过"
        return 0
    else
        log_error "网络连通性检查失败，无法ping通目标主机"
        return 1
    fi
}

get_vm_memory_info() {
    local src_host=$1
    local vm_name=$2
    
    local vm_mem_kb=$(ssh $src_host "virsh dominfo $vm_name | grep 'Used memory' | awk '{print \$3}'")
    local vm_mem_gb=$(( (vm_mem_kb + 1024*1024 - 1) / (1024*1024) ))
    local hugepage_used=$(ssh $src_host "virsh dumpxml $vm_name | grep -c '<memoryBacking>'")
    
    echo "$vm_mem_gb $hugepage_used"
}

check_target_memory() {
    local dst_host=$1
    local vm_mem_gb=$2
    local hugepage_used=$3
    
    if [ "$hugepage_used" -eq 1 ]; then
        log_info "虚拟机使用大页，检查目标主机大页情况..."
        
        local hugepage_info=$(ssh $dst_host "cat /proc/meminfo | grep Huge")
        local hugepages_total=$(echo "$hugepage_info" | grep HugePages_Total | awk '{print $2}')
        local hugepages_free=$(echo "$hugepage_info" | grep HugePages_Free | awk '{print $2}')
        local hugepage_size=$(echo "$hugepage_info" | grep Hugepagesize | awk '{print $2}')
        
        log_info "目标主机大页信息："
        log_info "  总大页数: $hugepages_total"
        log_info "  空闲大页数: $hugepages_free"
        log_info "  单大页大小: $hugepage_size kB"
        
        local hugepage_size_mb=$((hugepage_size / 1024))
        local required_hugepages=$(( (vm_mem_gb * 1024 + hugepage_size_mb - 1) / hugepage_size_mb ))
        
        log_info "虚拟机需要大页数: $required_hugepages"
        
        if [ "$hugepages_free" -lt "$required_hugepages" ]; then
            log_error "目标主机空闲大页数不足，需要 $required_hugepages 个，可用 $hugepages_free 个"
            return 1
        else
            log_info "目标主机大页数量充足"
            return 0
        fi
    else
        log_info "虚拟机不使用大页，检查目标主机可用内存..."
        
        local free_mem_gb=$(ssh $dst_host "free -g | grep Mem | awk '{print \$7}'")
        
        log_info "目标主机可用内存: $free_mem_gb GB"
        log_info "虚拟机需要内存: $vm_mem_gb GB"
        
        if [ "$free_mem_gb" -lt "$vm_mem_gb" ]; then
            log_error "目标主机可用内存不足，需要 $vm_mem_gb GB，可用 $free_mem_gb GB"
            return 1
        else
            log_info "目标主机内存充足"
            return 0
        fi
    fi
}

