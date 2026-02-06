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
