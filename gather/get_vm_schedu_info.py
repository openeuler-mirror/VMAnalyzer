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
        
        for domain in all_doms:
            vm_name = domain.name()
            vm_data = {"name": vm_name}
            
            sched_type = domain.schedulerType()
            vm_data["scheduler_type"] = sched_type
            
            sched_params = domain.schedulerParameters()
            vm_data["scheduler_params"] = {param: value for param, value in sched_params.items()}
            
            print(f"正在处理虚拟机：{vm_name}")
            
            try:
                job_info = domain.jobInfo()
                vm_data["dom_job_info"] = {
                    "job_type": job_info[0],
                    "job_status": job_info[1],
                    "job_data": job_info[2],
                    "job_time": job_info[3]
                }
            except libvirt.libvirtError:
                vm_data["dom_job_info"] = {"status": "No active job"}
            
            try:
                iothreads = domain.ioThreadInfo()
                io_thread_list = []
                for iothread in iothreads:
                    io_thread_list.append({
                        "iothread_id": iothread[0],
                        "cpu_affinity": list(iothread[1])
                    })
                vm_data["io_thread_info"] = io_thread_list
            except libvirt.libvirtError as e:
                vm_data["io_thread_info"] = {"error": str(e)}
            
            vm_data_list.append(vm_data)
        
        try:
            with open("vm_scheduler_info.json", "w", encoding="utf-8") as f:
                json.dump(vm_data_list, f, ensure_ascii=False, indent=2)
            print(f"数据已成功写入 vm_scheduler_info.json，共处理 {len(vm_data_list)} 台虚拟机")
        except IOError as e:
            print(f"写入文件失败：{str(e)}")

            
    except libvirt.libvirtError as e:
        print(f"libvirt 错误：{e}")
    finally:
        if 'conn' in locals() and conn is not None:
            conn.close()

if __name__ == "__main__":
    main()
