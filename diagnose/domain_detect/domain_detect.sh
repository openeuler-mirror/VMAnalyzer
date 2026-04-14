#!/bin/sh
set -euo pipefail

TOOLS_ROOT=$(cd $(dirname $0); pwd)
domain_detect_dir=/var/log/vmanalyzer/
datafile=${domain_detect_dir}domain_detect.json
check_arry_basic=(domain_state interface_link blk_error)
check_arry_premium=(domain_state disk_status interface_link blk_error)
check_arry=()

usage() {
    echo "domain_detect: auto detect domain availability"
    echo "options: -h,          help information"
    echo "         -e <string>, basic edition or premium edition"
    echo "         -d <string>, domain name, id or uuid"
}

if [ $# -eq 0 ]; then
    usage
    exit -1
fi

while getopts 'd:h:e:*' OPT; do
    case $OPT in
        "h")
            usage
            exit 0
            ;;
        "e")
            edition=$OPTARG
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

mk_log_dir() {
    if [ ! -d "$domain_detect_dir" ];then
        mkdir -p $domain_detect_dir
    fi
}

check_project() {
    sudo echo -e "{\"domain_detect\": {" > $datafile

    if [[ $edition == "basic" ]];then
        check_arry=("${check_arry_basic[@]}")
    else
        check_arry=("${check_arry_premium[@]}")
    fi
  
    let arry_len=${#check_arry[@]}-1
    for i in `seq 0 $arry_len`;
    do  
        if [ $i != $arry_len ];then
            sudo echo " \"${check_arry[$i]}\": {`sudo sh $TOOLS_ROOT/detect_domain_availability.sh $domain ${check_arry[$i]}`},">> $datafile
        else
            sudo echo " \"${check_arry[$i]}\": {`sudo sh $TOOLS_ROOT/detect_domain_availability.sh $domain ${check_arry[$i]}`}">> $datafile
        fi  
    done
    sudo echo "}}" >> $datafile
    sudo sed -i ':a;N;$!ba;s/\n//g' $datafile
}

mk_log_dir

check_project

