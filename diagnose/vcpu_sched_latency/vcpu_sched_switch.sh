#!/bin/bash

main() {
    local vm_name=$1
    local vcpu_id=$2

    if [ -z "$vm_name" ] || [ -z "$vcpu_id" ]; then
        log "ERROR" "Usage: $0 <VM_NAME> <VCPU_ID>"
        exit 1
    fi

    echo "VM Name: $vm_name"
    echo "vCPU ID: $vcpu_id"
}

main "$1" "$2"
