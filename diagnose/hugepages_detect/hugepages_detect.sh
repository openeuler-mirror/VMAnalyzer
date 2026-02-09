#!/bin/bash

HUGEPAGE_NODE_CONF_PATH="/etc/Hugepages_node.conf"
LOG_PATH="/var/log/hugetlb_pre.log"

# Insert section block
SECTION="\e[1;33m"
NORMAL="\e[0;39m"
YELLOW_BLINK="\e[1;33m"
RED="\e[1;31m"
NICLISTS=""
RLNICS=""

function warn_info()
{
    echo -e "${YELLOW_BLINK} Notice:${NORMAL} ${RED}$1 ${NORMAL}" >> $LOG_PATH
}

function err_info()
{
    time=`date +"%Y-%m-%d %H:%M:%S"`
    echo -e "$time ${YELLOW_BLINK} Error:${NORMAL} ${RED}$1 ${NORMAL}" >> $LOG_PATH
}

function log()
{
    time=`date +"%Y-%m-%d %H:%M:%S"`
    echo -e "\e[1m $time $1 \e[0;39m" >> $LOG_PATH
    echo ""
}

# 检测宿主机各节点大页数量
function record_node_hugepages()
{
    numanode_size=`numactl --hardware | grep "node .* size" | wc -l`
    for((i=0;i<$numanode_size;i++));
    do
        nid=$i
        hugepagesize_list=`ls /sys/devices/system/node/node$nid/hugepages/ | grep -oE '[0-9]+'`
        if [ x"" = x"hugepagesize_list" ]; then
             err_info "no hugepages resource pool!"
            return 1
        fi
        for hugepagesize in ${hugepagesize_list[@]};
        do
            nr_hugepages=`cat "/sys/devices/system/node/node$nid/hugepages/$hugepagesize/nr_hugepages"`
            free_hugepages=`cat "/sys/devices/system/node/node$nid/hugepages/$hugepagesize/free_hugepages"`
            used_hugepages=$(($nr_hugepages-$free_hugepages))
            log "node$nid hugepages-$hugepagesizekB HugePages_Total: $nr_hugepages"
            log "node$nid hugepages-$hugepagesizekB HugePages_Free: $free_hugepages"
            log "node$nid hugepages-$hugepagesizekB HugePages_Used: $used_hugepages"
        done
    done
    return 0
}

# 检测运行中虚机大页占用
function record_vm_hugepages()
{
    running_vms=`virsh list --all | grep running |awk '{print $2}'`
    if [ x"" = x"running_vms" ]; then
        err_info "no running vms！"
        return 1
    fi
    for vm in ${running_vms[@]}
    do
        pid=`ps -ef | grep qemu | grep $vm | awk '{print $2}'`
        total_2M=`grep -B 11 'KernelPageSize: 2048 kB' /proc/$pid/smaps | grep "^Size:" | awk 'BEGIN{sum=0}{sum+=$2}END{print sum/1024}'`
        total_1G=`grep -B 11 'KernelPageSize: 1048576 kB' /proc/$pid/smaps | grep "^Size:" | awk 'BEGIN{sum=0}{sum+=$2}END{print sum/1048576}'`
        log "$vm occupied $total_2M M, occupied $total_1G G /n"
    done
}

function check_allocate_flag()
{
    if [ -f "/tmp/hugepage_flag" ]; then
        error_num1=`cat /tmp/hugepage_flag`
        if [ $error_num1 -ne 0 ]; then
            err_info "allocate_hugepag script exec failed, please check."
            record_node_hugepages()
            record_vm_hugepages()
            exit 1
        fi
    else
        err_info "cannot find allocate_flag, the allocate_hugepag script may have problems! "
        record_node_hugepages()
        record_vm_hugepages()
        exit 1
    fi
}
