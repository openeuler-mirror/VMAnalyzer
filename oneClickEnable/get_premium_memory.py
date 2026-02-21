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
                LOG_INFO("libvirt 连接成功（qemu:///system）")
                return conn
            raise Exception("libvirt 连接失败，未获取到连接句柄")
        except libvirt.libvirtError as e:
            LOG_ERROR(f"libvirt 连接异常：{str(e)}")
            raise

    def get_vm_domain(self, vm_name: str) -> libvirt.virDomain:
        if vm_name in self.domains:
            return self.domains[vm_name]
        
        try:
            dom = self.conn.lookupByName(vm_name)
            self.domains[vm_name] = dom
            LOG_INFO(f"成功获取虚拟机 {vm_name} 句柄")
            return dom
        except libvirt.libvirtError as e:
            LOG_ERROR(f"获取虚拟机 {vm_name} 句柄失败：{str(e)}")
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
                raise Exception(f"虚拟机非运行状态（状态码：{vm_state}），QGA 命令无法执行")

            LOG_INFO(f"执行 QGA 命令：{self.QGA_MEMORY_CMD}")
            start_time = time.time()
            output = libvirt_qemu.qemuAgentCommand(dom, self.QGA_MEMORY_CMD, 30 * 1000, 0)
            LOG_INFO(f"QGA 命令执行成功，耗时：{time.time() - start_time:.2f} 秒")

            output_json = json.loads(output)
            LOG_INFO(f"QGA 原始返回：{json.dumps(output_json, indent=2)}")

            if "return" not in output_json:
                raise Exception("QGA 返回格式异常，缺失 'return' 字段")

        except Exception as e:
            error_msg = str(e)
            memory_status["error_msg"] = error_msg
            LOG_ERROR(f"执行 QGA 命令失败：{error_msg}")

        return memory_status
