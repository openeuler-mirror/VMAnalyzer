#! /bin/bash
# Program:
# This program is used to moniter system.
# History:
# Dinglimin Create 

# 日志
virt_dir=/var/log/vmanalyzer/

# 配置文件
TOOLS_ROOT=/usr/bin/vm_analyer/diagnose/virt_check
spectre_file=${TOOLS_ROOT}/spectre-meltdown-checker.sh
spectre_log=${virt_dir}spectre-meltdown-checker-basic-`date "+%Y-%m-%d-%H-%M-%S"`.log
default_config=${TOOLS_ROOT}/basic-config.env

declare -A dic=(
    [os_version]=系统版本
    [kernel]=内核版本
    [iommu]=Iommu配置
    [kernel_hot_patch]=内核热补丁
    [spectre_meltdown]=幽灵熔断漏洞
    [tuned]=Tuned配置
)

SYSTEM_TYPE=`uname -p`
source $default_config
source /etc/os-release

#Generate log file
mk_log_dir() {
    if [ ! -d "$virt_dir" ];then
        mkdir -p $virt_dir
    fi
}

log() {
    # 打印信息
    check_name_cn=${dic[$1]}
    sudo echo "{\"PROJECT\":\"$check_name_cn\",\"LOG\":\"$2\"}," >> $hostfile
}

# 系统信息
check_os_func() {
    #sudo echo "--------------------system information------------------------" >> $hostfile
    log "os_version" "系统版本:$VERSION_ID"
}

# 内核信息
check_kernel_func() {
    #sudo echo "--------------------kernel information------------------------" >> $hostfile
    # 查看内核版本
    kernel_ver=`sudo uname -r | egrep -o $Kernel_regex`
    log "kernel" "内核版本:$kernel_ver"

    # 查看内核参数
    Hygon=`grep '^vendor_id'  "/proc/cpuinfo" | awk '{print $3}' | head -1|grep HygonGenuine`

    # 查看是否开启iommu
    iommu_flag_x86=`sudo cat /proc/cmdline|grep intel_iommu=on`
    amd_iommu_flag_x86=`sudo cat /proc/cmdline|grep amd_iommu=on`
    pt_flag=`sudo cat /proc/cmdline|grep iommu=pt`
    iommu_flag_aarch64=`sudo cat /proc/cmdline|grep iommu.passthrough=1`

    if [ "${SYSTEM_TYPE}" == "aarch64" ]; then
        if [ ! -n "$iommu_flag_aarch64" ]; then
            log "iommu" "未开启iommu,建议开启iommu"
        else
            log "iommu" "已开启iommu"
        fi
    else
        if [ "${Hygon}x" != "x" ]; then
            if [ -n "$amd_iommu_flag_x86" ] && [ -n "$pt_flag" ]; then
                log "iommu" "已开启iommu"
            else
                log "iommu" "未开启iommu,建议开启iommu"
            fi
        else
            if [ -n "$iommu_flag_x86" ] && [ -n "$pt_flag" ]; then
                log "iommu" "已开启iommu"
            else
                log "iommu" "未开启iommu,建议开启iommu"
            fi
        fi
    fi

    # 查看内核热补丁
    sudo which kpatch >/dev/null 2>&1
    if [ $? -eq 0 ];then
        num=$(sudo kpatch list 2>/dev/null | grep enabled | wc -l)
        if [ $num -eq 0 ];then
            log "kernel_hot_patch" "不存在内核热补丁"
        else
            patches=`sudo kpatch list 2>/dev/null | grep enabled`
            patches_list=`sudo echo "$patches" |awk -F"[" ' {print $1}'`
            log "kernel_hot_patch" "已打$num个内核热补丁,补丁:$patches_list"
        fi
    else
        log "kernel_hot_patch" "不存在内核热补丁"
    fi

    # 漏洞检测
    if [[ -f $spectre_file ]]; then
        sudo bash $spectre_file > $spectre_log

        cve_num=`sudo grep -rn STATUS $spectre_log | wc -l`
        status_num=`sudo grep -rn "NOT VULNERABLE" $spectre_log | wc -l`
        if [[ $cve_num != $status_num ]]; then
            log "spectre_meltdown" "安全漏洞Spectre与Meltdown检测异常"
        else
            log "spectre_meltdown" "安全漏洞Spectre与Meltdown检测正常"
        fi
    else
        log "spectre_meltdown" "没有安全漏洞Spectre与Meltdown检测脚本,跳过检测"
    fi

    # 查看tuned-adm配置
    tuned=`sudo tuned-adm active | awk -F": " '{print $2}'`
    log "tuned" "tuned配置:$tuned"
}

usage() {
        echo "basic.sh: basic virtualization os config health check"
        echo "options: -h,          help information"
        echo "         -f <string>, host or domain"
        echo "         -d <string>, If -f is used to set domain, set the domain name,id or uuid"
}

while getopts 'd:f:h:*' OPT; do
        case $OPT in
                "h")
                        usage
                        exit 0
                        ;;
                "f")
                        flag=$OPTARG
                        ;;
                "d")
                        domain=$OPTARG
                        ;;
                *)
                        usage
                        exit -1
                ;;
        esac
done

mk_log_dir

case $flag in
    host)
        hostfile=${virt_dir}host_health_basic_`date "+%Y-%m-%d-%H-%M-%S"`.log
    ;;
    domain)
        hostfile=${virt_dir}domain_health_basic_`date "+%Y-%m-%d-%H-%M-%S"`.log
    ;;
    *)
    usage
    ;;
esac

# Exit success
exit 0
