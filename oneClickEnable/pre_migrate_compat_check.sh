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
	# The -1 is used to achieve ceiling division in Bash integer arithmetic, ensuring that the 
	# number of hugepages allocated is sufficient to cover the entire memory requirement and 
	# preventing VM startup failures due to insufficient pages.
        if [ "$hugepage_size_mb" -eq 0 ]; then
            log_error "解析大页大小异常，不可为0"
            return 1
        fi
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

main() {
    check_command ssh
    check_command scp
    check_command bc

    if [ $# -ne 3 ]; then
        echo "用法: $0 <源主机> <目标主机> <虚拟机名称>"
        echo "示例: $0 source-host dest-host vm1"
        exit 1
    fi

    src_host=$1
    dst_host=$2
    vm_name=$3

    log_info "开始虚拟机迁移前兼容性检查"
    log_info "源主机: $src_host"
    log_info "目标主机: $dst_host"
    log_info "虚拟机名称: $vm_name"

    check_source_to_target_network $src_host $dst_host
    net_result=$?

    if [ $net_result -eq 0 ]; then
        log_info "获取源端虚拟机 $vm_name 的内存信息..."
        read vm_mem_gb hugepage_used <<< $(get_vm_memory_info $src_host $vm_name)
        log_info "虚拟机内存大小: $vm_mem_gb GB"
        log_info "是否使用大页: $hugepage_used"

        check_target_memory $dst_host $vm_mem_gb $hugepage_used
        mem_result=$?

        if [ $mem_result -ne 0 ]; then
            exit 1
        fi

        src_info=$(ssh $src_host "bash -s" << EOF
libvirt_rpm=\$(rpm -qa | grep -E '^libvirt-[0-9]' | head -1)
if [ -n "\$libvirt_rpm" ]; then
    src_libvirt_ver=\$(echo \$libvirt_rpm | sed -E 's/^libvirt-([0-9]+\.[0-9]+\.[0-9]+-[0-9]+\.[0-9]+).*/\1/')
else
    src_libvirt_ver=""
fi

qemu_rpm=\$(rpm -qa | grep -E '^qemu-[0-9]' | head -1)
if [ -n "\$qemu_rpm" ]; then
    src_qemu_ver=\$(echo \$qemu_rpm | sed -E 's/^qemu-([0-9]+\.[0-9]+\.[0-9]+-[0-9]+\.[0-9]+).*/\1/')
else
    src_qemu_ver=""
fi

vm_xml=\$(virsh dumpxml $vm_name)

echo "SRC_LIBVIRT_VER:\$src_libvirt_ver"
echo "SRC_QEMU_VER:\$src_qemu_ver"
echo "VM_XML:\$vm_xml"
EOF
        )

        src_libvirt_ver=$(echo "$src_info" | grep "SRC_LIBVIRT_VER:" | cut -d':' -f2-)
        src_qemu_ver=$(echo "$src_info" | grep "SRC_QEMU_VER:" | cut -d':' -f2-)
        vm_xml=$(echo "$src_info" | sed -n '/VM_XML:/,$p' | sed '1s/VM_XML://')

        dst_info=$(ssh $dst_host "bash -s" << 'EOF'
libvirt_rpm=$(rpm -qa | grep -E '^libvirt-[0-9]' | head -1)
if [ -n "$libvirt_rpm" ]; then
    dst_libvirt_ver=$(echo $libvirt_rpm | sed -E 's/^libvirt-([0-9]+\.[0-9]+\.[0-9]+-[0-9]+\.[0-9]+).*/\1/')
else
    dst_libvirt_ver=""
fi

qemu_rpm=$(rpm -qa | grep -E '^qemu-[0-9]' | head -1)
if [ -n "$qemu_rpm" ]; then
    dst_qemu_ver=$(echo $qemu_rpm | sed -E 's/^qemu-([0-9]+\.[0-9]+\.[0-9]+-[0-9]+\.[0-9]+).*/\1/')
else
    dst_qemu_ver=""
fi

virsh domcapabilities > /tmp/dst_domcapabilities.xml
domcapabilities=$(cat /tmp/dst_domcapabilities.xml)

echo "DST_LIBVIRT_VER:$dst_libvirt_ver"
echo "DST_QEMU_VER:$dst_qemu_ver"
echo "DOMCAPABILITIES:$domcapabilities"
rm -rf /tmp/dst_domcapabilities.xml
EOF
        )

        dst_libvirt_ver=$(echo "$dst_info" | grep "DST_LIBVIRT_VER:" | cut -d':' -f2-)
        dst_qemu_ver=$(echo "$dst_info" | grep "DST_QEMU_VER:" | cut -d':' -f2-)
        domcapabilities=$(echo "$dst_info" | sed -n '/DOMCAPABILITIES:/,$p' | sed '1s/DOMCAPABILITIES://')

        echo "$domcapabilities" > /tmp/dst_domcapabilities.xml

        log_info "检查源主机与目标主机libvirt、qemu版本..."
        log_info "源主机 libvirt 版本: $src_libvirt_ver, QEMU 版本: $src_qemu_ver"
        log_info "目标主机 libvirt 版本: $dst_libvirt_ver, QEMU 版本: $dst_qemu_ver"

        ver_result=0
        if [ -z "$src_libvirt_ver" ] || [ -z "$dst_libvirt_ver" ]; then
            log_error "无法获取libvirt版本信息"
            ver_result=1
        elif [ "$(printf '%s\n' "$src_libvirt_ver" "$dst_libvirt_ver" | sort -V | head -n1)" != "$dst_libvirt_ver" ]; then
            log_error "目标主机 libvirt 版本 ($dst_libvirt_ver) 低于源主机 ($src_libvirt_ver)"
            ver_result=1
        fi

        if [ -z "$src_qemu_ver" ] || [ -z "$dst_qemu_ver" ]; then
            log_error "无法获取QEMU版本信息"
            ver_result=1
        elif [ "$(printf '%s\n' "$src_qemu_ver" "$dst_qemu_ver" | sort -V | head -n1)" != "$dst_qemu_ver" ]; then
            log_error "目标主机 QEMU 版本 ($dst_qemu_ver) 低于源主机 ($src_qemu_ver)"
            ver_result=1
        fi

        if [ $ver_result -eq 0 ]; then
            log_info "libvirt、qemu版本检查通过"
        fi

        log_info "检查虚拟机配置与目标主机能力的兼容性..."

        vm_cpu_model=$(echo "$vm_xml" | grep -oP '<model[^>]*>\K[^<]+')
        if [ -n "$vm_cpu_model" ]; then
            if grep -q "<model usable='yes'>$vm_cpu_model</model>" /tmp/dst_domcapabilities.xml; then
                log_info "CPU模型 $vm_cpu_model 在目标主机上可用"
            else
                log_warn "CPU模型 $vm_cpu_model 在目标主机上不可用，可能需要调整"
            fi
        else
            log_info "未找到虚拟机CPU模型信息，跳过CPU模型兼容性检查"
        fi

        vm_emulator=$(echo "$vm_xml" | grep "<emulator" | awk -F'>' '{print $2}' | awk -F'<' '{print $1}')
        emulator_type=$(basename "$vm_emulator")
        emulator_check=$(ssh $dst_host "which $emulator_type > /dev/null 2>&1 && echo 'found' || echo 'not found'")

        domain_result=0
        if [ "$emulator_check" = "found" ]; then
            log_info "虚拟化类型 $emulator_type 在目标主机上可用"
        else
            log_error "虚拟化类型 $emulator_type 在目标主机上不可用"
            domain_result=1
        fi

        if [ $domain_result -eq 0 ]; then
            log_info "虚拟机配置与目标主机能力兼容性检查通过"
        fi

        if [ $ver_result -eq 0 ] && [ $domain_result -eq 0 ]; then
            log_info "所有兼容性检查通过，可以进行迁移"
            exit 0
        else
            log_warn "部分兼容性检查未通过，建议检查并解决问题后再进行迁移"
            exit 1
        fi
    fi
}

main "$@"
