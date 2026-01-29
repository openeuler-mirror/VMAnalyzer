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
