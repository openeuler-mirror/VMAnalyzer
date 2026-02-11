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

function get_number()
{
    local nid=$1
    local mem_type=$2
    sum=0
    itemlist=`cat ${HUGEPAGE_NODE_CONF_PATH} 2> /dev/null |grep -v '#' | grep "^$nid:.*:$mem_type="`
    #itemlist=`cat ${HUGEPAGE_NODE_CONF_PATH} 2> /dev/null |grep -v '#' | grep "^$nid:.*:$mem_type"`
    echo $itemlist
    # HUGEPAGE_NODE_CONF_PATH size check
    if [ x"" = x"$itemlist" ]; then
        if [ "$mem_type" == "RSV" ]; then
            return 0
        else
            log "$itemlist"
            err_info "Hugepages_node.conf format has problem , please checkout"
            return 1
        fi
    fi
    for item in ${itemlist[@]}
    do
        number=`echo "$item" | awk -F= '{print $2}'`
        echo "$number" | grep '^[0-9]\+$' | grep -v '^0[0-9]\+$' > /dev/null 2>&1
        if [ $? -ne 0 ] || [ "$number" -gt "$(/usr/bin/getconf UINT_MAX)" ]; then
            err_info "invalid item: $item"
            #/etc/Hugepages_node.conf数值设定报错检查
            err_info "please checkout hugepage setting count , the value should be [0 - max(uint32)]"
            return 1
        else
            #log "valid item: $item"
            sum=$(($sum+$number))
        fi
    done
    log "node $1: $2 hugepage is $sum"
    return 0
}

function check_each_node_hugepage()
{
    local hugepagesize=$1
    numanode_size=`numactl --hardware | grep "node .* size" | wc -l`
    for((i=0;i<$numanode_size;i++));do
        nid=$i
        if [ $hugepagesize == "hugepages-1048576kB" ]; then
            get_number $nid "1G"
            if [ $? -ne 0 ]; then
                err_info "node $nid: invalid 1G configuration, please check the operation"
                return 1
            fi
            num_1G_hugepages_sum=$sum
            set_nr_hugepages=`cat "/sys/devices/system/node/node$nid/hugepages/$hugepagesize/nr_hugepages"`
            if [ $num_1G_hugepages_sum -ne $set_nr_hugepages ]; then
                err_info "node$nid/hugepages/$hugepagesize/nr_hugepages system max-used is $set_nr_hugepages"
                return 1
            fi
        elif [ $hugepagesize == "hugepages-2048kB" ]; then
            get_number $nid "2M"
            if [ $? -ne 0 ]; then
                err_info "node $nid: invalid 2M configuration!"
                return 1
            else
                num_2M_hugepages_sum=$sum
                set_nr_hugepages=`cat "/sys/devices/system/node/node$nid/hugepages/$hugepagesize/nr_hugepages"`
                if [ $num_2M_hugepages_sum -ne $set_nr_hugepages ]; then
                    err_info "node$nid/hugepages/$hugepagesz/nr_hugepages system max-used is $set_nr_hugepages"
                    return 1
                fi
            fi
        else
            err_info "node $nid: invalid configuration,not 2M or 1G !"
            return 1
        fi
    done
    return 0
}

function check_main()
{
    check_allocate_flag
    sizelist=`cat ${HUGEPAGE_NODE_CONF_PATH} 2> /dev/null | grep "^[0-9].*" |awk -F= '{print $1}'| awk -F: '{print $3}' | awk '!a[$0]++'`
    if [ $? -ne 0 ]; then
        err_info "check -- error -- , get hugesize exec failed!"
        return 1
    fi
    # /etc/Hugepages_node.conf内容为空报错检查
    if [ x"" = x"$sizelist" ]; then
        err_info "check -- error -- , hugapage size undefine , please checkout "
        return 1
    fi
    for size in ${sizelist[@]}
    do
        if [ x"" = x"$size" ]; then
            err_info "check -- error -- , wrong format, please checkout"
        elif [ "$size" == "RSV" ]; then
            continue
        elif [ "$size" == "1G" ]; then
            size_set=`cat /proc/cmdline | grep " *hugepagesz=1G"`
            if [ -z "$size_set" ]; then
               err_info "check -- error -- , /proc/cmdline do not have 1G hugepage size !"
            else
               check_each_node_hugepage 'hugepages-1048576kB'
               error_num=$(($error_num+$?))
               if [ $? -ne 0 ]; then
                  err_info "check -- error -- , 1G hugepages check exception, please check the operation!"
               fi
            fi
        elif [ "$size" == "2M" ]; then
            size_set_2M=`cat /proc/cmdline | grep " *hugepagesz=2M"`
            if [ -z "$size_set_2M" ]; then
               err_info "check -- error -- , /proc/cmdline do not have 2M hugepage size !"
            else
               check_each_node_hugepage 'hugepages-2048kB'
               if [ $? -ne 0 ]; then
                  err_info "check -- error -- , 2M hugepages check exception, please check the operation!"
               fi
            fi
        fi
    done
}
