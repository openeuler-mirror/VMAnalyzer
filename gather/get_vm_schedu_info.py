#!/usr/bin/env python3
import libvirt
import json

def main():
    vm_data_list = []
    try:
        conn = libvirt.open()
        if conn is None:
            print("无法连接到 libvirt 守护进程！")
            return
        
        running_doms = conn.listDomainsID()
        all_doms = []
        
        for dom_id in running_doms:
            dom = conn.lookupByID(dom_id)
            all_doms.append(dom)
        
        inactive_dom_names = conn.listDefinedDomains()
        for dom_name in inactive_dom_names:
            dom = conn.lookupByName(dom_name)
            all_doms.append(dom)
            
    except libvirt.libvirtError as e:
        print(f"libvirt 错误：{e}")
    finally:
        if 'conn' in locals() and conn is not None:
            conn.close()

if __name__ == "__main__":
    main()
