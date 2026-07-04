# coding: utf-8
import libvirt
import libvirt_qemu
import json
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
LOG_INFO = logging.info
LOG_ERROR = logging.error

class QgaMemoryStatus:
    def __init__(self):
        self.conn = self._init_libvirt_conn()
        self.domains = {}
        self.QGA_MEMORY_CMD = '{"execute":"guest-get-memory-status"}'

    def _init_libvirt_conn(self) -> libvirt.virConnect:
        try:
            conn = libvirt.open("qemu:///system")
            if conn:
                LOG_INFO("Operation message")
                return conn
            raise Exception("Operation message")
        except libvirt.libvirtError as e:
            LOG_ERROR(f"libvirt 连接异常：{str(e)}")
            raise

    def get_vm_domain(self, vm_name: str) -> libvirt.virDomain:
        if vm_name in self.domains:
            return self.domains[vm_name]
        
        try:
            dom = self.conn.lookupByName(vm_name)
            self.domains[vm_name] = dom
            LOG_INFO(f"成功获取VM {vm_name} 句柄")
            return dom
        except libvirt.libvirtError as e:
            LOG_ERROR(f"获取VM {vm_name} 句柄失败：{str(e)}")
            raise

    def execute_qga_memory_cmd(self, vm_name: str) -> dict:
        memory_status = {
            "vm_name": vm_name,
            "status": "failed",
            "error_msg": "",
            "collect_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "memory_info": {}
        }

        try:
            dom = self.get_vm_domain(vm_name)

            vm_state = dom.state()[0]
            if vm_state != libvirt.VIR_DOMAIN_RUNNING:
                raise Exception(f"VM非运行状态（状态码：{vm_state}），QGA 命令无法执行")

            LOG_INFO(f"执行 QGA 命令：{self.QGA_MEMORY_CMD}")
            start_time = time.time()
            output = libvirt_qemu.qemuAgentCommand(dom, self.QGA_MEMORY_CMD, 30 * 1000, 0)
            LOG_INFO(f"QGA 命令执行成功，耗时：{time.time() - start_time:.2f} 秒")

            output_json = json.loads(output)
            LOG_INFO(f"QGA 原始返回：{json.dumps(output_json, indent=2)}")

            if "return" not in output_json:
                raise Exception("Operation message")

            memory_raw = output_json["return"]           
            total = memory_raw.get("total", 0)
            available = memory_raw.get("available", 0)
            memory_info = {
                "total_mb": round(total, 2),
                "used_mb": round(total - available, 2),
                "free_mb": round(memory_raw.get("free", 0), 2),
                "available_mb": round(available, 2),
                "usage_rate": round(((total - available) / total) * 100, 2) if total != 0 else 0.0
            }

            memory_status.update({
                "status": "success",
                "error_msg": "",
                "memory_info": memory_info
            })

        except Exception as e:
            error_msg = str(e)
            memory_status["error_msg"] = error_msg
            LOG_ERROR(f"执行 QGA 命令失败：{error_msg}")

        return memory_status

    def batch_execute(self, vm_names: list) -> list:
        results = []
        for vm_name in vm_names:
            LOG_INFO(f"\n===== 开始处理VM：{vm_name} =====")
            result = self.execute_qga_memory_cmd(vm_name)
            results.append(result)
        return results

    def close(self):
        if self.conn:
            self.conn.close()
            LOG_INFO("Operation message")

if __name__ == "__main__":
    qga_memory = QgaMemoryStatus()

    try:
        vm_name = "test-bclinux7.6-qga"
        single_result = qga_memory.execute_qga_memory_cmd(vm_name)
        print("\n" + "="*80)
        print(f"VM {vm_name} memory状态查询结果")
        print("="*80)
        print(f"查询时间：{single_result['collect_time']}")
        mem = single_result["memory_info"]
        print(f"总memory：{mem['total_mb']} MB")
        print(f"已用memory：{mem['used_mb']} MB")
        print(f"空闲memory：{mem['free_mb']} MB")
        print(f"可用memory：{mem['available_mb']} MB")
        print(f"memory使用率：{mem['usage_rate']} %")

    finally:
        qga_memory.close()

