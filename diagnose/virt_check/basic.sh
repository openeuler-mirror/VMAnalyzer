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
sysctl_config=${TOOLS_ROOT}/basic-config-sysctl.conf
auth_file=${TOOLS_ROOT}/libvirt-auth-config.sh
auth_log=${virt_dir}libvirt-auth-config-`date "+%Y-%m-%d-%H-%M-%S"`.log

# cpu core
final_core_list=()
# 常见cpu支持的内存频率
cpu_memory_frequency=('6248R 2933' '6148 2666' '5218 26667' '5118 2400')

declare -A dic=(
    [os_version]=系统版本
    [kernel]=内核版本
    [iommu]=Iommu配置
    [kernel_hot_patch]=内核热补丁
    [spectre_meltdown]=幽灵熔断漏洞
    [tuned]=Tuned配置
    [qemu_version]=Qemu版本
    [libvirt_version]=Libvirt版本
    [open_files]=最大打开文件数
    [sysctl_config]=sysctl配置
    [turbo_boost]=cpu睿频
    [cpu_module]=cpu模式
    [transparent_hugepage]=透明大页
    [hugepages]=静态大页
    [memory_frequency]=内存频率
    [libvirt_auth]=libvirt鉴权
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

check_config() {
    good=0
    bad=0
    array_name=()
    while read -r line; do
        # ignoring empty lines
        if [ "$line" == "" ]; then
            continue
        fi
        # ignoring comments
        if echo "$line" | grep -qE '^#'; then
            continue
        fi
        refname=$(echo "$line" | cut -d' ' -f1)
        refpara=$(echo "$line" | awk -F '= ' '{print $(NF)}')
        cur=$(sysctl -n "$refname")

        if [ "$refpara" == "$cur" ];then
            good=$((good + 1))
        else
            array_name[${bad}]=${refname}
            bad=$((bad + 1))
        fi
    done < "$sysctl_config"
    if [ "$bad" == "0" ]; then
        log "$1" "sysctl的参数配置正常"
    else
        para=`echo ${array_name[@]}`
        log "$1" "sysctl参数[$para]，请检查是否需要修改"
    fi
}

# 系统信息
check_os_func() {
    #sudo echo "--------------------system information------------------------" >> $hostfile
    log "os_version" "系统版本:$VERSION_ID"
}

# 内核信息
check_kernel_func() {
    #sudo echo "--------------------kernel information------------------------" >> $hostfile
    # 1.查看内核版本
    kernel_ver=`sudo uname -r | egrep -o $Kernel_regex`
    log "kernel" "内核版本:$kernel_ver"

    # 查看内核参数
    Hygon=`grep '^vendor_id'  "/proc/cpuinfo" | awk '{print $3}' | head -1|grep HygonGenuine`

    # 2.查看是否开启iommu
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

    # 3.查看内核热补丁
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

    # 4.漏洞检测
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

    # 5.查看tuned-adm配置
    tuned=`sudo tuned-adm active | awk -F": " '{print $2}'`
    log "tuned" "tuned配置:$tuned"
}

# 宿主机虚拟化版本
check_virt_version_func() {
    #sudo echo "--------------------Virt Version------------------------" >> $hostfile
    #qemu_ver=`sudo qemu-img --v | awk NR==1 | cut -d '(' -f 1 | egrep -o $version_regex`
    qemu_ver=`sudo rpm -qa qemu-img | egrep -o $version_regex`
    libvirt_ver=`sudo rpm -qa libvirt | egrep -o $version_regex`

    [[ $qemu_ver == "" ]] && qemu_ver="没有安装Qemu"
    [[ $libvirt_ver == "" ]] && libvirt_ver="没有安装Libvirt"

    log "qemu_version" "Qemu版本:$qemu_ver"
    log "libvirt_version" "Libvirt版本:$libvirt_ver"
}

# 虚拟化配置检测
check_virt_config_func() {
    #sudo echo "--------------------Virt Config------------------------" >> $hostfile
    # 查看最大打开文件数
    #current_open_files=`sudo ulimit -n`
    libvirtd_pid=`pidof libvirtd`
    current_open_files=`cat /proc/$libvirtd_pid/limits | grep "Max open files" | awk '{print $4}'`
    if [[ "$current_open_files" == "$Open_Files" ]]; then
        log "$open_files" "最大打开文件个数:$current_open_files"
    else
        log "open_files" "最大打开文件个数:$current_open_files,建议设置大于或者等于$Open_Files"
    fi
}

# 查看sysctl配置
check_sysctl_config_func() {
check_config sysctl_config
}

# CPU信息
check_cpu_func(){
    #sudo echo "--------------------CPU information------------------------" >> $hostfile
    # 1、查看宿主机CPU是否开启睿频
    if [ ! -e "/sys/devices/system/cpu/intel_pstate/no_turbo" ]; then
        log "turbo_boost" "不支持睿频"
    else
        no_turbo_flag=`sudo cat /sys/devices/system/cpu/intel_pstate/no_turbo`
        if [[ $no_turbo_flag == "0" ]];then
            log "turbo_boost" "睿频开启"
        else
            log "turbo_boost" "睿频关闭"
        fi
    fi
    # 2、查看宿主机CPU模式
    cpufreq=`sudo cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor`
    [[ $cpufreq == "" ]] && cpufreq="无法获取CPU性能模式"
    log "cpu_module" "cpu性能模式:$cpufreq"
}

# 宿主机大页信息
check_huge_page_func(){
    #sudo echo "--------------------Host hugepage infomation------------------------" >> $hostfile
    # 1、查看宿主机透明大页情况
    flag=`sudo cut -d "]" -f 1 /sys/kernel/mm/transparent_hugepage/enabled | awk -F "[" '{print $2}'`
    if [[ $flag == $THP_flag ]]; then
        log "transparent_hugepage" "已开启透明大页"
    else
        log "transparent_hugepage" "透明大页未开启"
    fi
    # 2、查看宿主机静态大页情况
    hug=`cat /sys/kernel/mm/hugepages/hugepages-*/nr_hugepages`
    hug_num=0
    while read -r line;
    do
      if [[ $line -ne 0 ]];then
          hug_num=$(($hug_num+1))
      fi
    done<<<`cat /sys/kernel/mm/hugepages/hugepages-*/nr_hugepages`
    if [[ $hug_num -ne 0 ]]; then
        log "hugepages" "已配置大页内存"
    else
        log "hugepages" "没有配置大页内存"
    fi
}

# 内存检测
check_memory_func(){
    speed_list=()
    support_list=()

    # 查看宿主机内存信息
    #sudo echo "--------------------Host memory information------------------------" >> $hostfile

    # 1、获取实际内存频率
    speed=`sudo dmidecode -t memory | grep -i "Configured Clock Speed" |grep -v Unknown`
    for i in "${speed}"
    do
        speed_list=`sudo echo $i | tr -cd "[0-9]"`
    done

    # 2、查看内存最大支持的频率
    support=`sudo dmidecode|grep -A16 "Memory Device"|grep 'Speed' |grep -v Unknown`
    for i in "${support}"
    do
        support_list=`sudo echo $i | tr -cd "[0-9]"`
    done

    # 3、查看是否内存降频
    model=$(grep 'model name' /proc/cpuinfo | head -n 1 | cut -d ':' -f 2 | xargs)
    bad_num=0
    for j in ${speed_list[@]};do
        for k in ${support_list[@]};do
            let num1=$k-$j
            num1=${num1/-/}
            if [[ $num1 -gt $Mem_Frequency ]];then
                for g in "${cpu_memory_frequency[@]}" ; do
                    echo $model |grep ${g[@]:1:1}
                    if [ $? -eq 0 ];then
                        let num2=$j-${g[@]:2:1}
                        num2=${num2/-/}
                        if [[ $num2 -gt $Mem_Frequency ]];then
                            bad_num=$((bad_num + 1))
                        fi
                    fi
                done
            fi
        done
    done
    if [[ $bad_num != 0 ]];then
        log "memory_frequency" "内存频率降频，请检查下内存"
    else
        log "memory_frequency" "内存频率正常"
    fi
}

# 鉴权检测
check_auth_func(){
    if [[ -f ${auth_file} ]]; then
        sudo bash $auth_file check &>$auth_log
        sudo cat $auth_log | grep -i "libvirt auth is set" &>/dev/null
        if [ $? -eq 0 ];then
            log "libvirt_auth" "libvirt开启鉴权"
        else
            log "libvirt_auth" "libvirt没有开启鉴权"
        fi
    else
        log "libvirt_auth" "没有libvirt鉴权检测脚本,跳过检测"
    fi
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
