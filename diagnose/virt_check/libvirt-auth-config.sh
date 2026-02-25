#! /bin/bash
# Program:
# This program is used to libvirt auth.
# History:
# Dinglimin Create the file.

URL="tcp://127.0.0.1/system"
PACKAGE_NAME=(cyrus-sasl cyrus-sasl-devel cyrus-sasl-lib cyrus-sasl-md5 cyrus-sasl-plain cyrus-sasl-gssapi)

LIBVIRTD_FILE=/etc/libvirt/libvirtd.conf
declare -A LIBVIRTD_CONF=([listen_tls]="0" [listen_tcp]="1" [auth_tcp]="sasl")

SASL_PATH=/etc/sasl2
SASL_LIBVIRT_FILE=${SASL_PATH}/libvirt.conf
declare -A SASL_LIBVIRT_CONF=([mech_list]="digest-md5" [sasldb_path]="/etc/libvirt/passwd.db")

SASL_QEMU_FILE=(qemu.conf qemu-kvm.conf)
SYSCONFIG_LIBVIRT_FILE=/etc/sysconfig/libvirtd
declare -A SYSCONFIG_LIBVIRT_CONF=([LIBVIRTD_ARGS]="--listen")

TOOLS_ROOT=/usr/bin/vm_analyer/diagnose/virt_check
default_config=${TOOLS_ROOT}/premium-config.env

source $default_config

set_check_config() {
    if [ "$1" == $LIBVIRTD_FILE ]; then
        for key in $(sudo echo ${!LIBVIRTD_CONF[*]}) ; do
            cur=$(sudo grep ^${key} $1 | awk -F '=' '{ print $NF }')
            if [[ $(sudo echo $cur | sed 's/\"//g') != ${LIBVIRTD_CONF[$key]} ]];then
                if [ $2 == true ]; then
                    sudo echo "set $1 config failed"
                    exit 1
                else
                    if [[ $(sudo echo $cur | sed 's/\"//g') != "" ]];then
                        if [ $key == auth_tcp ]; then
                            sudo sed -i "/^$key/c\\$key = \"${LIBVIRTD_CONF[$key]}\"" $1
                        else
                            sudo sed -i "/^$key/c\\$key = ${LIBVIRTD_CONF[$key]}" $1
                        fi
                    else
                        sudo echo "$key = \"${LIBVIRTD_CONF[$key]}\"" |sudo tee -a $1
                    fi
                fi
            fi
        done
    elif [ "$1" == $SASL_LIBVIRT_FILE ]; then
        for key in $(sudo echo ${!SASL_LIBVIRT_CONF[*]}) ; do
            cur=$(sudo grep ^${key} $1 | awk -F ':' '{ print $NF }')
            if [[ $(sudo echo $cur | sed 's/\"//g') != ${SASL_LIBVIRT_CONF[$key]} ]];then
                if [ $2 == true ]; then
                    sudo echo "set $1 config failed"
                    exit 1
                else
                    if [[ $(sudo echo $cur | sed 's/\"//g') != "" ]];then
                        sudo sed -i "/^$key/c\\$key:${SASL_LIBVIRT_CONF[$key]}" $1
                    else
                        sudo echo "$key:${SASL_LIBVIRT_CONF[$key]}" |sudo tee -a $1
                    fi
                fi
            fi
        done
    else
        for key in $(sudo echo ${!SYSCONFIG_LIBVIRT_CONF[*]}) ; do
            cur=$(sudo grep ^${key} $1 | awk -F '=' '{ print $NF }')
            if [[ $(sudo echo $cur | sed 's/\"//g') != ${SYSCONFIG_LIBVIRT_CONF[$key]} ]];then
                if [ $2 == true ]; then
                    sudo echo "set $1 config failed"
                    exit 1
                else
                    if [[ $(sudo echo $cur | sed 's/\"//g') != "" ]];then
                        sudo sed -i "/^$key/c\\$key = \"${SYSCONFIG_LIBVIRT_CONF[$key]}\"" $1
                    else
                        sudo echo "$key = \"${SYSCONFIG_LIBVIRT_CONF[$key]}\"" |sudo tee -a $1
                    fi
                fi
            fi
        done
    fi
}

set_auth() {
    # install sasl package
    for name in "${PACKAGE_NAME[@]}" ; do
        sudo rpm -qa |grep -w $name
            if [ $? -ne 0 ]; then
                 sudo yum install -y $name --nogpgcheck
                 sudo rpm -qa |grep -w $name
                 if [ $? -ne 0 ]; then
                         sudo echo "can not install $name"
                         exit 1
                 fi
            fi
    done
    #set /etc/libvirt/libvirtd.conf
    sudo cp -a -f ${LIBVIRTD_FILE} ${LIBVIRTD_FILE}_bak
    set_check_config ${LIBVIRTD_FILE} false
    set_check_config ${LIBVIRTD_FILE} true
    #set /etc/sasl2/libvirt.conf
    sudo cp -a -f ${SASL_LIBVIRT_FILE} ${SASL_LIBVIRT_FILE}_bak
    set_check_config ${SASL_LIBVIRT_FILE} false
    set_check_config ${SASL_LIBVIRT_FILE} true
    #set /etc/sysconfig/libvirtd
    sudo cp -a -f ${SYSCONFIG_LIBVIRT_FILE} ${SYSCONFIG_LIBVIRT_FILE}_bak
    set_check_config ${SYSCONFIG_LIBVIRT_FILE} false
    set_check_config ${SYSCONFIG_LIBVIRT_FILE} true

}

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
