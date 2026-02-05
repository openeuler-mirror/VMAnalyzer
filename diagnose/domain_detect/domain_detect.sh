#!/bin/sh

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
