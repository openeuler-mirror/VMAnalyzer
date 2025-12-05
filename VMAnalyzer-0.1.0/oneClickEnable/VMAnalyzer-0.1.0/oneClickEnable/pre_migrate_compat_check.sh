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
        # 直接在源主机上生成完整的CPU XML文件并复制到本地
        ssh $src_host "virsh capabilities | grep -A 100 '<cpu' | grep -B 100 '</cpu>' > /tmp/src_cpu.xml"
        scp $src_host:/tmp/src_cpu.xml /tmp/
        
        # 从源主机获取其他信息
        src_info=$(ssh $src_host "bash -s" << EOF
            # 获取libvirt版本，只匹配libvirt-数字开头的包
            libvirt_rpm=\$(rpm -qa | grep -E '^libvirt-[0-9]' | head -1)
            # 提取版本号：libvirt-8.0.0-5.63.oe2203.bclinux.x86_64 -> 8.0.0-5.63
            if [ -n "\$libvirt_rpm" ]; then
                src_libvirt_ver=\$(echo \$libvirt_rpm | sed -E 's/^libvirt-([0-9]+\.[0-9]+\.[0-9]+-[0-9]+\.[0-9]+).*/\1/')
            else
                src_libvirt_ver=""
            fi
            
            # 获取qemu版本，只匹配qemu-数字开头的包
            qemu_rpm=\$(rpm -qa | grep -E '^qemu-[0-9]' | head -1)
            # 提取版本号：qemu-6.2.0-44.89.oe2203.bclinux.x86_64 -> 6.2.0-44.89
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
        
        # 解析源主机信息
        src_libvirt_ver=$(echo "$src_info" | grep "SRC_LIBVIRT_VER:" | cut -d':' -f2-)
        src_qemu_ver=$(echo "$src_info" | grep "SRC_QEMU_VER:" | cut -d':' -f2-)
        vm_xml=$(echo "$src_info" | sed -n '/VM_XML:/,$p' | sed '1s/VM_XML://')
        
        # 从目标主机获取所有所需信息
        dst_info=$(ssh $dst_host "bash -s" << 'EOF'
            # 获取libvirt版本，只匹配libvirt-数字开头的包
            libvirt_rpm=$(rpm -qa | grep -E '^libvirt-[0-9]' | head -1)
            # 提取版本号：libvirt-8.0.0-5.63.oe2203.bclinux.x86_64 -> 8.0.0-5.63
            if [ -n "$libvirt_rpm" ]; then
                dst_libvirt_ver=$(echo $libvirt_rpm | sed -E 's/^libvirt-([0-9]+\.[0-9]+\.[0-9]+-[0-9]+\.[0-9]+).*/\1/')
            else
                dst_libvirt_ver=""
            fi
            
            # 获取qemu版本，只匹配qemu-数字开头的包
            qemu_rpm=$(rpm -qa | grep -E '^qemu-[0-9]' | head -1)
            # 提取版本号：qemu-6.2.0-44.89.oe2203.bclinux.x86_64 -> 6.2.0-44.89
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
EOF
        )
        
        # 解析目标主机信息
        dst_libvirt_ver=$(echo "$dst_info" | grep "DST_LIBVIRT_VER:" | cut -d':' -f2-)
        dst_qemu_ver=$(echo "$dst_info" | grep "DST_QEMU_VER:" | cut -d':' -f2-)
        domcapabilities=$(echo "$dst_info" | sed -n '/DOMCAPABILITIES:/,$p' | sed '1s/DOMCAPABILITIES://')
        
        # 保存domcapabilities到临时文件
        echo "$domcapabilities" > /tmp/dst_domcapabilities.xml
        
        # 检查libvirt和qemu版本
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
        
        # 使用本地文件进行CPU兼容性检查
        log_info "检查CPU兼容性..."
        cpu_compare_result=$(cat /tmp/src_cpu.xml | ssh $dst_host "virsh cpu-compare /dev/stdin 2>&1")
        
        cpu_result=0
        if grep -q "CPU is compatible" <<< "$cpu_compare_result"; then
            log_info "CPU兼容性检查通过"
        else
            log_warn "CPU兼容性检查警告："
            echo "$cpu_compare_result"
            cpu_result=1
        fi
        
        # 检查虚拟机配置与目标主机能力的兼容性
        log_info "检查虚拟机配置与目标主机能力的兼容性..."
        
        vm_cpu_model=$(echo "$vm_xml" | grep -A 1 "<cpu mode=" | grep "<model" | awk -F'"' '{print $2}')
        if grep -q "<model usable='yes'>$vm_cpu_model</model>" /tmp/dst_domcapabilities.xml; then
            log_info "CPU模型 $vm_cpu_model 在目标主机上可用"
        else
            log_warn "CPU模型 $vm_cpu_model 在目标主机上不可用，可能需要调整"
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
        
        # 汇总结果
        if [ $ver_result -eq 0 ] && [ $cpu_result -eq 0 ] && [ $domain_result -eq 0 ]; then
            log_info "所有兼容性检查通过，可以进行迁移"
            exit 0
        else
            log_warn "部分兼容性检查未通过，建议检查并解决问题后再进行迁移"
            exit 1
        fi
    else
        exit 1
    fi
}

main "$@"
