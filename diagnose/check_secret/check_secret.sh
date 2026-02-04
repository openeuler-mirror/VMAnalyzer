#!/bin/bash
# Program:
# This program is used to check secret list.
# History:
# Dinglimin Create the file.

virt_dir=/var/log/vmanalyzer/

mk_log_dir() {
    if [ ! -d "$virt_dir" ]; then
        mkdir -p $virt_dir
    fi
}

info() {
    echo "{\"status\": \"info\", \"log\": \"$1\"}" >> $check_log
}

error() {
    echo "{\"status\": \"error\", \"log\": \"$1\"}" >> $check_log
}

warn() {
    echo "{\"status\": \"warning\", \"log\": \"$1\"}" >> $check_log
}

check_log=${virt_dir}check_secret-$(date "+%Y-%m-%d-%H-%M-%S").log

# 主函数
main() {
    mk_log_dir
    echo "####################################################################################" > $check_log
    time=$(date +"%Y-%m-%d %H:%M:%S")
    echo "$time" >> $check_log
}

# 执行主函数
main
