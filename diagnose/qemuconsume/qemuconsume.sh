#!/bin/sh
#****************************************************************#
# ScriptName: qemuconsume.sh
# Author: DingLimin
# Function:
#***************************************************************#

CURDATE=$(date "+%Y-%m-%d-%H-%M-%S")
qemuconsume_dir=/var/log/vmanalyzer/

usage() {
    echo "qemuconsume: show qemu-kvm process consumption"
    echo "options: -h,          help information"
}

while getopts 'h' OPT; do
    case $OPT in
        "h")
            usage
            exit 0
            ;;
        *)
            usage
            exit -1
            ;;
    esac
done

# placeholder for main logic
echo "Script initialized at $CURDATE"
