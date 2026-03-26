# VMAnalyzer API 完整文档

## 概述

VMAnalyzer 提供了一套完整的 API 用于虚拟化监控，包括采集、存储、分析和报告等功能。

## 核心模块 API

### 1. 采集模块 (agent/collector.py)

#### VMStatsCollector 类

虚拟机统计信息采集器，负责从 libvirt 获取各项指标。

```python
from agent.collector import VMStatsCollector

# 创建采集器实例
collector = VMStatsCollector(vm_factory, stats_storage, label='cpuUsage')

# 开始采集
collector.record_stats()
```

**构造函数参数：**
| 参数 | 类型 | 说明 |
|------|------|------|
| vm_factory | VMFactory | 虚拟机工厂实例 |
| stats_storage | VMStatsStorage | 存储接口实例 |
| label | str | 采集标签，如 'cpuUsage', 'memoryUsage' |

**主要方法：**

- `record_stats()` - 采集并记录所有虚拟机的统计信息
- `_send_qga_command(dom, cmd_dict)` - 发送 QEMU Guest Agent 命令
- `_exec_guest_command(dom, shell_cmd)` - 在虚拟机内执行 shell 命令

#### 采集标签类型

| 标签 | 说明 |
|------|------|
| `cpuUsage` | CPU 使用率 |
| `memoryUsage` | 内存使用率 |
| `networkTraffic` | 网络流量统计 |
| `blkio` | 块设备 I/O |
| `log_vm` | 虚拟机日志 |

---

### 2. 虚拟机管理模块 (agent/vm.py)

#### VMFactory 类

虚拟机工厂，统一管理所有虚拟机实例。

```python
from agent.vm import VMFactory

# 创建工厂实例
factory = VMFactory(uri='qemu:///system')

# 获取所有虚拟机
vms = factory.get_all_vms()

# 获取特定虚拟机
vm = factory.get_vm_by_uuid(uuid)
```

**主要方法：**

| 方法 | 返回值 | 说明 |
|------|--------|------|
| `get_all_vms()` | List[Domain] | 获取所有虚拟机 |
| `get_vm_by_uuid(uuid)` | Domain | 通过 UUID 获取虚拟机 |
| `get_vm_by_name(name)` | Domain | 通过名称获取虚拟机 |
| `scan_active_vms()` | None | 扫描活动虚拟机 |

#### 全局 VM 实例

```python
from agent import vm

# 获取全局虚拟机工厂
vm_factory = vm.vm_factory

# 获取所有活动虚拟机
active_vms = vm.active_vms
```

---

### 3. 存储模块 (agent/storage.py)

#### VMStatsRedisStorage 类

基于 Redis 的指标存储实现。

```python
from agent.storage import VMStatsRedisStorage

# 创建存储实例
storage = VMStatsRedisStorage(vm_factory, label='cpuUsage')

# 检查连接
ok, err_msg = storage.check_connection()

# 保存指标
storage.save_metrics(vm_uuid, metrics)

# 获取指标
metrics = storage.get_metrics(vm_uuid)
```

**主要方法：**

| 方法 | 参数 | 说明 |
|------|------|------|
| `check_connection()` | - | 检查 Redis 连接 |
| `save_metrics(vm_uuid, metrics)` | vm_uuid, dict | 保存指标数据 |
| `get_metrics(vm_uuid)` | str | 获取指标数据 |
| `delete_metrics(vm_uuid)` | str | 删除指标数据 |

**配置选项：**

```python
# Redis 配置
REDIS_CONFIG = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'password': None,
    'socket_timeout': 5,
    'socket_connect_timeout': 5
}
```

---

### 4. 分析模块 (agent/analyze.py)

#### VMStatsAnalyze 类

虚拟机统计分析器，提供性能分析和告警功能。

```python
from agent.analyze import VMStatsAnalyze

# 创建分析器
analyzer = VMStatsAnalyze(vm_factory, label='cpuUsage')

# 分析特定虚拟机
analysis = analyzer.analyze_vm(vm_uuid)

# 获取所有告警
alerts = analyzer.get_all_alerts()
```

**分析方法：**

| 方法 | 返回值 | 说明 |
|------|--------|------|
| `analyze_vm(vm_uuid)` | dict | 分析单个虚拟机 |
| `get_cpu_analysis(vm_uuid)` | dict | CPU 分析 |
| `get_memory_analysis(vm_uuid)` | dict | 内存分析 |
| `get_all_alerts()` | List[dict] | 获取所有告警 |

**告警类型：**

```python
ALERT_TYPES = {
    'cpu_high': 'CPU 使用率过高',
    'memory_high': '内存使用率过高',
    'disk_high': '磁盘使用率过高',
    'network_drops': '网络丢包过多'
}
```

---

### 5. 报告模块 (agent/reporter.py)

#### VMAnalyzersReporter 类

报告生成器，定期生成性能报告。

```python
from agent.reporter import VMAnalyzersReporter

# 创建报告器
reporter = VMAnalyzersReporter(
    vm_factory=vm_factory,
    vm_storage=storage,
    vm_viewer=viewer,
    vm_analyzer=analyzer,
    interval=10
)

# 启动报告生成
reporter.start_report()
```

**报告格式：**

```json
{
    "timestamp": 1234567890,
    "vm_count": 5,
    "vms": [
        {
            "uuid": "vm-uuid-here",
            "name": "vm-name",
            "cpu_usage": 45.2,
            "memory_usage": 67.8,
            "status": "running"
        }
    ]
}
```

---

### 6. 展示模块 (agent/view.py)

#### VMAnalyzersConsoleView 类

控制台视图，用于在终端显示监控数据。

```python
from agent.view import VMAnalyzersConsoleView

# 创建控制台视图
view = VMAnalyzersConsoleView()

# 显示报告
view.display(report_data)
```

#### VMAnalyzersFileView 类

文件视图，将数据输出到文件。

```python
from agent.view import VMAnalyzersFileView

# 创建文件视图
view = VMAnalyzersFileView('/path/to/output.jsonl')

# 写入报告
view.display(report_data)
```

---

### 7. 事件模块 (agent/event.py)

#### VMEventLoopNative 类

本地事件循环，监听虚拟机生命周期事件。

```python
from agent.event import VMEventLoopNative

# 创建事件循环
event_loop = VMEventLoopNative(uri='qemu:///system')

# 启动事件监听
event_loop.start()

# 注册回调
event_loop.on_vm_started = lambda uuid: print(f"VM started: {uuid}")
event_loop.on_vm_stopped = lambda uuid: print(f"VM stopped: {uuid}")
```

**事件类型：**

| 事件 | 说明 |
|------|------|
| `VM_STARTED` | 虚拟机启动 |
| `VM_STOPPED` | 虚拟机停止 |
| `VM_PAUSED` | 虚拟机暂停 |
| `VM_RESUMED` | 虚拟机恢复 |
| `VM_DEFINED` | 虚拟机定义 |
| `VM_UNDEFINED` | 虚拟机取消定义 |

---

### 8. 工具模块 (utils/)

#### 定时器 (utils/timer.py)

```python
from utils.timer import RepeatedTimer

# 创建定时器
timer = RepeatedTimer(interval=5, function=my_function)

# 启动
timer.start()

# 停止
timer.stop()
```

#### 配置管理 (utils/config.py)

```python
from utils.config import REDIS_DATABASE_CONFIG

# 获取配置
redis_host = REDIS_DATABASE_CONFIG['host']
redis_port = REDIS_DATABASE_CONFIG['port']
```

---

## 完整使用示例

### 示例 1: 基本监控

```python
#!/usr/bin/env python
import time
from agent.vm import VMFactory
from agent.storage import VMStatsRedisStorage
from agent.collector import VMStatsCollector
from utils.timer import RepeatedTimer

# 初始化
vm_factory = VMFactory('qemu:///system')
storage = VMStatsRedisStorage(vm_factory, 'cpuUsage')
collector = VMStatsCollector(vm_factory, storage, 'cpuUsage')

# 启动采集（每5秒）
timer = RepeatedTimer(5, collector.record_stats)
timer.start()

# 运行一段时间
time.sleep(60)

# 停止
timer.stop()
```

### 示例 2: 自定义告警

```python
from agent.analyze import VMStatsAnalyze

analyzer = VMStatsAnalyze(vm_factory, 'cpuUsage')

# 设置自定义阈值
analyzer.set_threshold('cpu_usage', 80.0)
analyzer.set_threshold('memory_usage', 90.0)

# 分析并获取告警
for vm in vm_factory.get_all_vms():
    uuid = vm.UUIDString()
    analysis = analyzer.analyze_vm(uuid)
    
    if analysis['alerts']:
        print(f"VM {uuid} has alerts: {analysis['alerts']}")
```

### 示例 3: 导出数据到文件

```python
from agent.view import VMAnalyzersFileView
from agent.reporter import VMAnalyzersReporter

# 创建文件输出视图
viewer = VMAnalyzersFileView('/var/log/vm_metrics.jsonl')

# 创建报告器
reporter = VMAnalyzersReporter(
    vm_factory, storage, viewer, analyzer, interval=10
)

# 生成报告
reporter.start_report()
```

---

## 错误处理

### 常见异常

```python
from libvirt import libvirtError

try:
    vm_factory = VMFactory('qemu:///system')
except libvirtError as e:
    print(f"Failed to connect to libvirt: {e}")

# Redis 连接错误
try:
    storage = VMStatsRedisStorage(vm_factory, 'cpuUsage')
    ok, err = storage.check_connection()
    if not ok:
        print(f"Redis connection failed: {err}")
except Exception as e:
    print(f"Storage error: {e}")
```

---

## 性能优化建议

1. **采集间隔**：建议生产环境使用 5-10 秒间隔
2. **数据保留**：设置合理的 Redis 数据过期时间
3. **批量操作**：使用管道批量获取 Redis 数据
4. **连接池**：使用 Redis 连接池提高性能
