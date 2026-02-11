#! /bin/bash
# Program:
# This program is used to moniter system.
# History:
# Dinglimin Create the file.

usage() {
        echo "virt_health: virtualization os config health check"
        echo "options: -h,          help information"
        echo "         -e <string>, basic edition or premium edition"
        echo "         -f <string>, host or domain"
        echo "         -d <string>, If -f is used to set domain, set the domain name,id or uuid"
}

if [ $# -eq 0 ]; then
    usage
    exit -1
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
                        exit -1
                ;;
        esac
done

if [[ $edition == "premium" ]];then
    file_name="premium.sh"   
elif [[ $edition == "basic" ]];then
    file_name="basic.sh"
else
    echo "Only basic and premium are supported after the -e argument"
    exit -1
fi

exit 0
