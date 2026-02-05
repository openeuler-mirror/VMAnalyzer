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
