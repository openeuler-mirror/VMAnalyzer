#! /bin/bash
# Program:
# This program is used to moniter system.
# History:
# Dinglimin Create the file.

usage() {
    echo "virt_health: virtualization os config health check"
    echo "options: -h,          help information"
}

if [ $# -eq 0 ]; then
    usage
    exit -1
fi

exit 0
