#! /bin/bash
# Program:
# This program is used to moniter system.
# History:
# Dinglimin Create 

# 日志
virt_dir=/var/log/vmanalyzer/

# 配置文件
TOOLS_ROOT=/usr/bin/vm_analyer/diagnose/virt_check
default_config=${TOOLS_ROOT}/basic-config.env

declare -A dic=(
    [os_version]=系统版本
    [kernel]=内核版本
)

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
