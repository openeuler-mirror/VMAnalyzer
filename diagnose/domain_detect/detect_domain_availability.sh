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

# 检查qga是否连接
check_qga_state() {
    qga_status=`sudo virsh dumpxml $1 |grep "qemu.guest_agent" |grep -w "connected"`
    if [[ $? != 0 ]];then
        warn "云主机没有连接qga，跳过检查"
    fi
    
    sudo virsh qemu-agent-command $1 '{"execute":"guest-info"}' >/dev/null 2>&1
    if [[ $? != 0 ]];then
        warn "云主机没有连接qga，跳过检查"
    fi
}

# 检查qga cmd是否支持
check_qga_cmd() {
    sudo echo $* |grep "has not been found" >/dev/null
    if [[ $? == 0 ]];then
        warn "云主机qga不支持命令${13}，跳过检查"
    fi
}

# 查看云主机的状态
domain_state_func() {
    domain_state=`sudo virsh domstate $1 2>&1`

    sudo echo $domain_state |grep "Timed out" >/dev/null
    if [[ $? == 0 ]];then
        error "请求超时，获取云主机状态失败"
    fi

    if [[ $domain_state == "running" ]];then
        info "云主机运行状态正常"
    else
        error "云主机运行状态不正常" 
    fi
}

# 入参检查、开始检测
if [ $# -lt 2 ];then
    usage
fi

