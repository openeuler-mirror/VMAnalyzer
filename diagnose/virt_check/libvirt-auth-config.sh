#! /bin/bash
# Program:
# This program is used to libvirt auth.
# History:
# Dinglimin Create the file.

URL="tcp://127.0.0.1/system"
PACKAGE_NAME=(cyrus-sasl cyrus-sasl-devel cyrus-sasl-lib cyrus-sasl-md5 cyrus-sasl-plain cyrus-sasl-gssapi)

LIBVIRTD_FILE=/etc/libvirt/libvirtd.conf
SASL_PATH=/etc/sasl2
SASL_LIBVIRT_FILE=${SASL_PATH}/libvirt.conf
SASL_QEMU_FILE=(qemu.conf qemu-kvm.conf)
SYSCONFIG_LIBVIRT_FILE=/etc/sysconfig/libvirtd

TOOLS_ROOT=/usr/bin/vm_analyer/diagnose/virt_check
default_config=${TOOLS_ROOT}/premium-config.env

source $default_config

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
