# 性能调优指南

本文档提供 VMAnalyzer 的性能调优建议，帮助您在不同场景下获得最佳性能。

## 目录

- [概述](#概述)
- [采集频率调优](#采集频率调优)
- [Redis 性能优化](#redis-性能优化)
- [多虚拟机环境优化](#多虚拟机环境优化)
- [资源限制配置](#资源限制配置)
- [生产环境建议](#生产环境建议)

---

## 概述

VMAnalyzer 的性能主要受以下因素影响：

| 因素 | 影响 | 优化方向 |
|------|------|----------|
| 采集间隔 | CPU/IO 使用 | 延长间隔降低负载 |
| 虚拟机数量 | 并发采集压力 | 批量采集、连接池 |
| Redis 配置 | 数据存储性能 | 内存、持久化策略 |
| 数据保留时间 | 内存占用 | 缩短保留期 |

---

## 采集频率调优

### 开发/测试环境

```bash
# 高频采集，详细信息
vm-analyzer-agent -i 1 -d
```

**配置：**
- 采集间隔：1 秒
- 调试模式：开启
- 数据保留：1 小时

### 生产环境（轻负载）

```bash
# 平衡性能和数据粒度
vm-analyzer-agent -i 5
```

**配置：**
- 采集间隔：5 秒
- 调试模式：关闭
- 数据保留：1 小时

### 生产环境（重负载）

```bash
# 降低采集频率，减少系统开销
vm-analyzer-agent -i 10
```

**配置：**
- 采集间隔：10 秒
- 调试模式：关闭
- 数据保留：30 分钟

### 关键业务监控

```bash
# 针对关键 VM 高频采集
vm-analyzer-agent -i 2 -t 3600
```

---

## Redis 性能优化

### 内存优化

```python
# utils/config.py

# 方案 1：缩短数据保留时间
REDIS_RETENTION_SECONDS = 1800  # 30 分钟

# 方案 2：限制最大内存
REDIS_DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 6379,
    'socket_keepalive': True,
    'socket_keepalive_options': {},
}
```

### Redis 服务端配置

```bash
# /etc/redis/redis.conf

# 限制最大内存
maxmemory 256mb
maxmemory-policy allkeys-lru

# 禁用持久化（如果不需要）
save ""

# 启用压缩
rdbcompression yes
```

### 连接池优化

```python
# 使用连接池提高性能
import redis

pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    max_connections=50,
    retry_on_timeout=True,
    socket_keepalive=True
)

r = redis.Redis(connection_pool=pool)
```

---

## 多虚拟机环境优化

### 场景：100+ 虚拟机

**问题：** 大量 VM 并发采集导致系统负载高

**解决方案：**

1. **分批采集**
```python
# agent/collector.py 修改

class VMStatsCollector:
    def __init__(self, vm_factory, stats_storage, label, batch_size=10):
        self.batch_size = batch_size
        # ...
    
    def record_stats_batch(self):
        """分批采集降低瞬时压力"""
        vms = self.vm_factory.get_all_vms()
        
        for i in range(0, len(vms), self.batch_size):
            batch = vms[i:i + self.batch_size]
            self._record_batch(batch)
            time.sleep(0.1)  # 批次间短暂暂停
```

2. **增加采集间隔**
```bash
# 大量 VM 时适当延长间隔
vm-analyzer-agent -i 15
```

3. **分布式采集**
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Collector 1│     │  Collector 2│     │  Collector 3│
│  (VMs 1-30) │     │  (VMs 31-60)│     │  (VMs 61-90)│
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                    ┌──────┴──────┐
                    │   Redis     │
                    │   Cluster   │
                    └─────────────┘
```

---

## 资源限制配置

### 使用 systemd 限制资源

```ini
# /etc/systemd/system/vm-analyzer.service

[Unit]
Description=VM Analyzer Agent
After=redis.service libvirtd.service

[Service]
Type=simple
ExecStart=/usr/local/bin/vm-analyzer-agent -i 5
Restart=always

# CPU 限制（最多使用 50% 单核）
CPUQuota=50%

# 内存限制（最多 256MB）
MemoryLimit=256M

# 文件描述符限制
LimitNOFILE=4096

[Install]
WantedBy=multi-user.target
```

### 使用 cgroups v2

```bash
# 创建 cgroup
sudo mkdir -p /sys/fs/cgroup/vmanalyzer

# 设置 CPU 限制（50%）
echo "50000 100000" | sudo tee /sys/fs/cgroup/vmanalyzer/cpu.max

# 设置内存限制（256MB）
echo 268435456 | sudo tee /sys/fs/cgroup/vmanalyzer/memory.max

# 启动 agent 并加入 cgroup
sudo systemd-run --scope --property=Delegate=cpu,memory \
    --unit=vmanalyzer \
    --slice=vmanalyzer.slice \
    vm-analyzer-agent
```

---

## 生产环境建议

### 推荐配置

| 参数 | 小型环境 (<20 VM) | 中型环境 (20-100 VM) | 大型环境 (>100 VM) |
|------|-------------------|----------------------|---------------------|
| 采集间隔 | 5 秒 | 10 秒 | 15-30 秒 |
| Redis 内存 | 128 MB | 256 MB | 512 MB+ |
| 数据保留 | 2 小时 | 1 小时 | 30 分钟 |
| 批量大小 | 10 | 20 | 50 |
| 并发连接 | 20 | 50 | 100 |

### 监控指标

```python
# 监控 VMAnalyzer 自身性能
import psutil

def check_agent_health():
    process = psutil.Process()
    
    return {
        'cpu_percent': process.cpu_percent(),
        'memory_mb': process.memory_info().rss / 1024 / 1024,
        'connections': len(process.connections()),
        'threads': process.num_threads()
    }
```

### 高可用部署

```yaml
# docker-compose.yml
version: '3'

services:
  vmanalyzer-1:
    build: .
    command: vm-analyzer-agent -i 5
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
    restart: unless-stopped
    
  vmanalyzer-2:
    build: .
    command: vm-analyzer-agent -i 5
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
    restart: unless-stopped
    
  redis:
    image: redis:alpine
    command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru
    restart: unless-stopped
```

### 性能测试

```bash
# 测试不同配置下的资源使用

# 场景 1：低频率
time vm-analyzer-agent -i 10 -t 60 &
PID=$!
sleep 5
ps -p $PID -o %cpu,%mem,cmd
wait

# 场景 2：高频率
time vm-analyzer-agent -i 1 -t 60 &
PID=$!
sleep 5
ps -p $PID -o %cpu,%mem,cmd
wait
```

---

## 故障排查

### 性能问题诊断

```bash
# 1. 检查 Redis 延迟
redis-cli --latency

# 2. 检查 libvirt 响应时间
virsh -c qemu:///system list --all

# 3. 监控 agent 资源使用
pidstat -u -p $(pgrep vm-analyzer) 1

# 4. 检查系统负载
top -p $(pgrep vm-analyzer)
```

### 常见性能瓶颈

| 症状 | 原因 | 解决方案 |
|------|------|----------|
| CPU 使用率高 | 采集频率过高 | 增加 -i 参数值 |
| 内存使用增长 | Redis 数据堆积 | 缩短保留时间 |
| 采集延迟大 | 虚拟机响应慢 | 检查 QEMU Guest Agent |
| Redis 连接失败 | 连接数超限 | 使用连接池 |

---

## 最佳实践总结

1. **从小开始**：初始使用保守配置（10秒间隔），根据需要调整
2. **监控监控工具**：使用 VMAnalyzer 监控自身的资源使用
3. **定期清理**：设置合理的 Redis 数据过期策略
4. **分层采集**：关键 VM 高频采集，普通 VM 低频采集
5. **资源隔离**：使用 systemd/cgroups 限制资源使用
