#!/bin/sh
# Program:
# This program is used to detect domain availability.
# History:
# Dinglimin Create the file.

usage() {
    sudo echo $"usage: $0 {\$domain-uuid|\$domain-id|\$domain-name} {domain_state|disk_status|interface_link|blk_error}"
    exit 2
}

if [ $# -lt 2 ];then
    usage
fi
