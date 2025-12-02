#! /bin/bash
# Program:
# This program is used to moniter system.
# History:
# Dinglimin Create the file.

# Generate args
# 是否跨numa
across_flag=1
# 日志
virt_dir=/var/log/vmanalyzer/

# 配置文件
TOOLS_ROOT=/usr/bin/vm_analyer/diagnose/virt_check
spectre_file=${TOOLS_ROOT}/spectre-meltdown-checker.sh
spectre_log=${virt_dir}spectre-meltdown-checker-basic-`date "+%Y-%m-%d-%H-%M-%S"`.log
default_config=${TOOLS_ROOT}/basic-config.env
sysctl_config=${TOOLS_ROOT}/basic-config-sysctl.conf
# cpu core
final_core_list=()
# 常见cpu支持的内存频率
cpu_memory_frequency=('6248R 2933' '6148 2666' '5218 26667' '5118 2400')

declare -A dic=([os_version]=系统版本 [kernel]=内核版本 [iommu]=Iommu配置 [numa]=Numa配置 [kernel_hot_patch]=内核热补丁 [spectre_meltdown]=幽灵熔断漏洞 [tuned]=Tuned配置 [qemu_version]=Qemu版本 [libvirt_version]=Libvirt版本 [open_files]=最大打开文件数 [sysctl_config]=sysctl配置 [turbo_boost]=cpu睿频 [cpu_module]=cpu模式 [transparent_hugepage]=透明大页 [hugepages]=静态大页 [memory_frequency]=内存频率 [vcpus_cross]=虚拟机vcpu是否跨numa [numa_mode]=虚拟机numa配置 [cpu_mode]=虚拟机cpu_mode [dom_huge_page]=虚拟机大页 [dom_schedinfo]=虚拟机调度)

SYSTEM_TYPE=`uname -p`
source $default_config
source /etc/os-release

#Generate log file
mk_log_dir() {
    if [ ! -d "$virt_dir" ];then
        mkdir -p $virt_dir
    fi
}

#Generate the json file used by bclinux_om
generate_json(){
	[ -f "$datafile" ] && sudo rm -rf $datafile
	sudo \cp -rf $hostfile $datafile
	sudo sed -i ':a;N;$!ba;s/\n//g' $datafile
}

log() {
    # 打印信息
    check_name_cn=${dic[$1]}
    sudo echo "{\"PROJECT\":\"$check_name_cn\",\"LOG\":\"$2\"}," >> $hostfile
}

#public
Install_rpm() {
rpm_name=$1
install1=`sudo rpm -qa $rpm_name`
if [ ! -n "$install1" ]; then
    sudo yum install -y $rpm_name
    install2=`sudo rpm -qa $rpm_name`
    if [ ! -n "$install2" ]; then
        return 1
    fi
fi
return 0
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

remove_symbols() {
A=()
A=`sudo grep -nE "^]" $hostfile | awk -F ":" '{print$1}'`
for line in ${A[@]};do
    line_before=$((line - 1))
    sed -i "${line_before}s/.$//" $hostfile
done
}

#---------------------------------------------------------------------------------
#-------------------------------宿主机--------------------------------------------
# 一、系统信息
check_os_func() {
#sudo echo "--------------------system information------------------------" >> $hostfile
log "os_version" "系统版本:$VERSION_ID"
}

# 二、内核信息
check_kernel_func() {
#sudo echo "--------------------kernel information------------------------" >> $hostfile
# 1、查看内核版本
kernel_ver=`sudo uname -r | egrep -o $Kernel_regex`
log "kernel" "内核版本:$kernel_ver"

# 2、查看内核参数
Hygon=`grep '^vendor_id'  "/proc/cpuinfo" | awk '{print $3}' | head -1|grep HygonGenuine`

# 查看是否开启iommu
iommu_flag_x86=`sudo cat /proc/cmdline|grep intel_iommu=on`
pt_flag=`sudo cat /proc/cmdline|grep iommu=pt`
iommu_flag_aarch64=`sudo cat /proc/cmdline|grep iommu.passthrough=1`

if [ "${SYSTEM_TYPE}" == "aarch64" ]; then
    if [ ! -n "$iommu_flag_aarch64" ]; then
        log "iommu" "未开启iommu,建议开启iommu"
    else
        log "iommu" "已开启iommu"
    fi
else
    if [ -n "$iommu_flag_x86" ] && [ -n "$pt_flag" ]; then
        log "iommu" "已开启iommu"
    else
        log "iommu" "未开启iommu,建议开启iommu"
    fi
fi

