#!/bin/sh
# Program:
# This program is used to detect domain availability.
# History:
# Dinglimin Create the file.

# The script parameter:
# $0 : ./detect_domain_availability.sh
# $1 : $domain-uuid|\$domain-id|\$domain-name
# $2 : domain_state|filesystem_status|oom_status|disk_status|interface_link|blk_error
#  
# The script returns the following values:
# 0 : 结果正常
# 1 : 结果异常
# 2 ：参数错误/警告提示,跳过检查

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

# 1.查看云主机的状态
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

# 2.查看网卡状态
domain_interface_link_func() {
    interface=`sudo virsh domiflist $1 |awk -F " " 'NR>=3 {print $1}'`
    interface_num=`sudo echo $interface |awk -F " " '{print NF}'`
    if [[ $interface_num -gt 0 ]];then
        sudo virsh domiflist $1 |awk -F " " 'NR>=3 {print $1}' |grep -w "^-"
        if [[ $? == 0 ]];then
            warn "云主机的interface显示为-，无法判断网卡连接状态，请检查SDN版本"
        else
            array=(${interface// / })
            for var in ${array[@]}
            do
                interface_cmd=`sudo virsh domif-getlink $1 $var 2>&1`
                sudo echo $interface_cmd |grep "Timed out" >/dev/null
                if [[ $? == 0 ]];then
                    error "请求超时，获取云主机网卡连接状态失败"
                fi
                interface_status=`sudo echo $interface_cmd | awk -F " " '{print $2}'`
                if [[ $interface_status != "up" ]];then
                    error "Interface ${var} 连接状态是 ${interface_status}"
                fi
            done
        fi
    else
        error "云主机不存在网卡"
    fi
    info "Interface ${array[*]} 连接状态是 UP"
}

# 3.查看磁盘状态
domain_disk_status_func() {
    disk_cmd=`sudo virsh qemu-agent-command $1 '{"execute":"guest-user-check", "arguments": {"command-name":"check-fs", "command":"mount | egrep '/dev/[v,s]d'"}}' 2>&1`
    sudo echo $disk_cmd |grep "Timed out" >/dev/null
    if [[ $? == 0 ]];then
        error "请求超时，获取云主机磁盘状态失败"
    fi
    check_qga_cmd $disk_cmd
    disk_status=`sudo echo $disk_cmd | cut -d '(' -f2 | cut -d ')' -f1 |cut -d ',' -f1`
    if [[ $disk_status == "ro" ]];then
        error "云主机磁盘状态为只读"
    else
        info "云主机磁盘状态为读写" 
    fi
}

# 4.查看磁盘是否有error
domain_blk_error_func() {
    blk_error=`sudo virsh domblkerror $1 2>&1`
    sudo echo $blk_error |grep "Timed out" >/dev/null
    if [[ $? == 0 ]];then
        error "请求超时，查询云主机磁盘是否有error失败"    
    fi
    if [[ $blk_error == "No errors found" ]];then
        info "云主机磁盘没有error"
    else
        error "云主机磁盘存在error，error: ${blk_error}" 
    fi
}

# 入参检查、开始检测
if [ $# -lt 2 ];then
    usage
fi

case "$2" in
  domain_state)
    domain_state_func $1
    ;;
  disk_status)
    check_qga_state $1
    domain_disk_status_func $1
    ;;
  interface_link)
    domain_interface_link_func $1
    ;;
  blk_error)
    domain_blk_error_func $1
    ;;
  *)
    usage
    ;;
esac
