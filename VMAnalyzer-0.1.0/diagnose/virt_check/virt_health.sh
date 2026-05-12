#! /bin/bash
# Program:
# This program is used to moniter system.
# History:
# Dinglimin Create the file.

# Generate args
# 返回值
ret=0
# 日志
virt_dir=/var/log/vmanalyzer/
# 配置文件
TOOLS_BIN=/usr/bin/vm_analyer/diagnose/virt_check

usage() {
        echo "virt_health: virtualization os config health check"
        echo "options: -h,          help information"
        echo "         -e <string>, basic edition or premium edition"
        echo "         -f <string>, host or domain"
        echo "         -d <string>, If -f is used to set domain, set the domain name,id or uuid"
}

if [ $# -eq 0 ]; then
       usage
       exit 1
fi

while getopts 'd:f:e:h:*' OPT; do
        case $OPT in
                "h")
                        usage
                        exit 0
                        ;;
                "e")
                        edition=$OPTARG
                        ;;
                "f")
                        flag=$OPTARG
                        ;;
                "d")
                        domain=$OPTARG
                        ;;
                *)
                        usage
                        exit 1
                ;;
        esac
done

if [[ $edition == "premium" ]];then
    file_name="premium.sh"   
elif [[ $edition == "basic" ]];then
    file_name="basic.sh"
else
    echo "Only basic and premium are supported after the -e argument"
    exit 1
fi

script_path="$TOOLS_BIN/$file_name"
if [ ! -f "$script_path" ]; then
    echo "Error: $script_path not found"
    exit 1
fi

if [ $flag == "domain" ];then
    sudo sh $TOOLS_BIN/$file_name -f $flag -d $domain
else
    sudo sh $TOOLS_BIN/$file_name -f $flag
fi
ret=`echo $?`

# Exit 
exit $ret
