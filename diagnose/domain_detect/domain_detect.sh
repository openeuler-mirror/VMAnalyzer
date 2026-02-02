#!/bin/sh

TOOLS_ROOT=$(cd $(dirname $0); pwd)
domain_detect_dir=/var/log/vmanalyzer/
datafile=${domain_detect_dir}domain_detect.json
check_arry_basic=(domain_state interface_link blk_error)
check_arry_premium=(domain_state disk_status interface_link blk_error)
check_arry=()
