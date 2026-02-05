#! /bin/bash
# Program:
# This program is used to moniter system.
# History:
# Dinglimin Create 

# 日志
virt_dir=/var/log/vmanalyzer/

#Generate log file
mk_log_dir() {
    if [ ! -d "$virt_dir" ];then
        mkdir -p $virt_dir
    fi
}

usage() {
        echo "basic.sh: basic virtualization os config health check"
        echo "options: -h,          help information"
        echo "         -f <string>, host or domain"
        echo "         -d <string>, If -f is used to set domain, set the domain name,id or uuid"
}

while getopts 'd:f:h:*' OPT; do
        case $OPT in
                "h")
                        usage
                        exit 0
                        ;;
                "f")
                        flag=$OPTARG
                        ;;
                "d")
                        domain=$OPTARG
                        ;;
                *)
                        usage
                        exit -1
                ;;
        esac
done

mk_log_dir

case $flag in
    host)
        hostfile=${virt_dir}host_health_basic_`date "+%Y-%m-%d-%H-%M-%S"`.log
    ;;
    domain)
        hostfile=${virt_dir}domain_health_basic_`date "+%Y-%m-%d-%H-%M-%S"`.log
    ;;
    *)
    usage
    ;;
esac

# Exit success
exit 0

