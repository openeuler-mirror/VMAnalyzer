#!/bin/sh
# Program:
# This program is used to detect domain availability.
# History:
# Dinglimin Create the file.

usage() {
    sudo echo $"usage: $0 {\$domain-uuid|\$domain-id|\$domain-name} {domain_state|disk_status|interface_link|blk_error}"
    exit 2
}

# 日志输出
info() {
    # 打印正常信息，正常退出 
    sudo echo "\"status\": \"info\", \"log\": \"$1\"" 
    exit 0
}

error() { 
    # 打印出错信息，异常退出 
    sudo echo "\"status\": \"error\", \"log\": \"$1\"" 
    exit 1 
} 

warn() {
    # 打印警告信息，异常退出 
    sudo echo "\"status\": \"warning\", \"log\": \"$1\""
    exit 2 
}

# 入参检查、开始检测
if [ $# -lt 2 ];then
    usage
fi
