#! /bin/bash
# Program:
# This program is used to libvirt auth.
# History:
# Dinglimin Create the file.

usage() {
    sudo echo "usage: $0 <set/fallback/check>"
    exit 1
}

case $1 in
    set|fallback|check)
        ;;
    *)
        usage
        ;;
esac

# Exit success
exit 0
