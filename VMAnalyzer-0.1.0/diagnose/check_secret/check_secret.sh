#!/bin/bash
# Program:
# This program is used to check secret list.
# History:
# Dinglimin Create the file.

# 日志
virt_dir=/var/log/vmanalyzer/

# 日志目录创建
mk_log_dir() {
    if [ ! -d "$virt_dir" ]; then
        mkdir -p $virt_dir
    fi
}

# 日志输出
info() {
    # 打印正常信息
    echo "{\"status\": \"info\", \"log\": \"$1\"}" >> $check_log
}

error() {
    # 打印出错信息
    echo "{\"status\": \"error\", \"log\": \"$1\"}" >> $check_log
}

warn() {
    # 打印警告信息
    echo "{\"status\": \"warning\", \"log\": \"$1\"}" >> $check_log
}

# 配置文件
check_log=${virt_dir}check_secret-$(date "+%Y-%m-%d-%H-%M-%S").log

# 检查密钥是否被使用
check_secret_usage() {
    info "Checking secret usage..."

    # 获取所有密钥的 UUID
    SECRET_UUIDS=$(virsh secret-list | awk '{print $1}' | grep -E '^[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}$')

    for SECRET_UUID in $SECRET_UUIDS; do
        info "Checking secret UUID: $SECRET_UUID"

        # 标志位，用于判断密钥是否被使用
        KEY_USED=false

        # 获取所有虚拟机名称
        VM_LIST=$(virsh list --all --name)

        # 遍历每个虚拟机
        for VM_NAME in $VM_LIST; do
            # 获取虚拟机的 XML 配置
            VM_XML=$(virsh dumpxml "$VM_NAME")

            # 检查虚拟机是否使用了该密钥
            if echo "$VM_XML" | grep -q "$SECRET_UUID"; then
                info "Secret UUID $SECRET_UUID is used in VM: $VM_NAME"
                KEY_USED=true

                # 提取磁盘路径
                DISK_PATHS=$(echo "$VM_XML" | grep -oP '(?<=<source file=\").*?(?=\")')
                for DISK_PATH in $DISK_PATHS; do
                    info "Disk path: $DISK_PATH"
                done
            fi
        done

        # 如果密钥未被使用，记录错误
        if [ "$KEY_USED" = false ]; then
            error "Secret UUID $SECRET_UUID is not used in any VM (invalid key)."
        fi
    done

    info "Secret usage check completed."
}

# 检查密钥的唯一性
check_secret_uniqueness() {
    info "Checking secret uniqueness..."

    # 获取所有密钥的 UUID
    SECRET_UUIDS=$(virsh secret-list | awk '{print $1}' | grep -E '^[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}$')

    for SECRET_UUID in $SECRET_UUIDS; do
        info "Checking secret UUID: $SECRET_UUID"

        # 获取密钥的 XML 文件路径
        SECRET_XML="/etc/libvirt/secrets/$SECRET_UUID.xml"
        if [ ! -f "$SECRET_XML" ]; then
            error "Secret XML file not found for UUID $SECRET_UUID."
            continue
        fi

        # 解析 XML 文件，获取配置的虚拟机名称
        VM_NAME=$(grep -oP '(?<=<description>).*?(?=</description>)' "$SECRET_XML")
        if [ -z "$VM_NAME" ]; then
            error "No VM name found in secret XML for UUID $SECRET_UUID."
            #continue
        else 
            info "Secret UUID $SECRET_UUID is configured for VM: $VM_NAME"
        fi

        # 检查是否有其他虚拟机使用了该密钥
        VM_LIST=$(virsh list --all --name)
        for VM in $VM_LIST; do
            if [ "$VM" != "$VM_NAME" ]; then
                VM_XML=$(virsh dumpxml "$VM")
                if echo "$VM_XML" | grep -q "$SECRET_UUID"; then
                    error "Secret UUID $SECRET_UUID is used in VM: $VM"
                fi
            fi
        done
    done

    info "Secret uniqueness check completed."
}

# 检查密钥的权限和所有者
check_secret_permissions() {
    info "Checking secret permissions..."

    # 获取所有密钥的 UUID
    SECRET_UUIDS=$(virsh secret-list | awk '{print $1}' | grep -E '^[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}$')

    for SECRET_UUID in $SECRET_UUIDS; do
        info "Checking secret UUID: $SECRET_UUID"

        # 获取密钥的 XML 文件路径
        SECRET_XML="/etc/libvirt/secrets/$SECRET_UUID.xml"
        if [ ! -f "$SECRET_XML" ]; then
            error "Secret XML file not found for UUID $SECRET_UUID."
            continue
        fi

        # 检查文件权限
        PERMISSIONS=$(stat -c "%A" "$SECRET_XML")
        if [ "$PERMISSIONS" != "-rw-------" ]; then
            error "Secret XML file for UUID $SECRET_UUID has incorrect permissions (expected 600)."
        fi

        # 检查文件所有者
        OWNER=$(stat -c "%U" "$SECRET_XML")
        if [ "$OWNER" != "root" ]; then
            error "Secret XML file for UUID $SECRET_UUID has incorrect owner (expected root)."
        fi

        info "Secret UUID $SECRET_UUID has correct permissions and owner."
    done

    info "Secret permissions check completed."
}

# 清理未使用的僵尸秘钥
clean_zombie_secrets() {
    info "Start cleaning zombie secrets (not used by any VM)..."

    SECRET_UUIDS=$(virsh secret-list 2>/dev/null | awk '{print $1}' | grep -E '^[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}$')

    for SECRET_UUID in $SECRET_UUIDS; do
        IS_USED=false

        virsh list --all --name 2>/dev/null | while read -r VM_NAME; do
            [ -z "$VM_NAME" ] && continue
            VM_XML=$(virsh dumpxml "$VM_NAME" 2>/dev/null)
            if echo "$VM_XML" | grep -q "$SECRET_UUID"; then
                IS_USED=true
            fi
        done

        if [ "$IS_USED" = false ]; then
            warn "Found zombie secret: $SECRET_UUID, preparing to undefine..."
            
            virsh secret-undefine "$SECRET_UUID" 2>/dev/null
            if [ $? -eq 0 ]; then
                info "Successfully cleaned zombie secret: $SECRET_UUID"
            else
                error "Failed to clean zombie secret: $SECRET_UUID"
            fi
        fi
    done

    info "Zombie secret clean completed."
}

# 主函数
main() {
    mk_log_dir
    echo "####################################################################################" > $check_log
    time=$(date +"%Y-%m-%d %H:%M:%S")
    echo "$time" >> $check_log

    # 执行检查
    check_secret_permissions
    check_secret_usage
    check_secret_uniqueness

    clean_zombie_secrets

    # 错误汇总
    ERROR_COUNT=$(grep -c '"status": "error"' "$check_log")
    if [ "$ERROR_COUNT" -gt 0 ]; then
        echo "Check completed with $ERROR_COUNT error(s). See log file for details: $check_log"
        exit 1
    else
        echo "Check completed successfully. No errors found."
        exit 0
    fi
}

# 执行主函数
main
