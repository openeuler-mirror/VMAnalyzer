#! /bin/bash
# Program: 
# This program is used to detect domain availability. 
# History: 
# Dinglimin Create the file.

# The script parameter:
# $0 : ./detect_domain_availability.sh
# $1 : $domain-uuid|\$domain-id|\$domain-name
# $2 : domain_state
#  
# The script returns the following values:
# 0 : 结果正常
# 1 : 结果异常
# 2 ：参数错误/警告提示,跳过检查

# 使用例子
usage() {
    sudo echo $"usage: $0 {\$domain-uuid|\$domain-id|\$domain-name} {domain_state}"
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


######项目检测######
# 1、查看云主机的状态
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

case "$2" in
  domain_state)
    domain_state_func $1
    ;;
  *)
    usage
    ;;
esac

