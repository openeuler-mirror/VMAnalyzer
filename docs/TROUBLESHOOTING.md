# 故障排查指南

本文档提供 VMAnalyzer 常见问题的详细排查步骤和解决方案。

## 目录

- [安装问题](#安装问题)
- [连接问题](#连接问题)
- [采集问题](#采集问题)
- [性能问题](#性能问题)
- [Redis 问题](#redis-问题)
- [权限问题](#权限问题)

---

## 安装问题

### 问题：pip 安装失败

**症状：**
```
ERROR: Could not find a version that satisfies the requirement...
```

**排查步骤：**

1. 检查 Python 版本
```bash
python3 --version
# 需要 Python 3.6+
```

2. 检查 pip 版本
```bash
pip3 --version
# 建议升级到最新版本
pip3 install --upgrade pip
```

3. 检查依赖包
```bash
# 安装系统依赖
sudo yum install -y python3-devel libvirt-devel gcc

# Ubuntu/Debian
sudo apt-get install -y python3-dev libvirt-dev gcc
```

**解决方案：**
```bash
# 使用虚拟环境
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

---

### 问题：找不到 libvirt 模块

**症状：**
```
ModuleNotFoundError: No module named 'libvirt'
```

**排查步骤：**

1. 检查系统 libvirt 安装
```bash
# 检查 libvirtd 服务
systemctl status libvirtd

# 检查 libvirt 客户端
virsh --version
```

2. 检查 Python libvirt 绑定
```bash
pip3 show libvirt-python
```

**解决方案：**
```bash
# 安装 libvirt-python
sudo pip3 install libvirt-python

# 或者通过包管理器
sudo yum install -y python3-libvirt
```

---

## 连接问题

### 问题：无法连接到 QEMU/KVM

**症状：**
```
Failed to connect to QEMU/KVM
```

**排查步骤：**

1. 检查 libvirtd 服务状态
```bash
sudo systemctl status libvirtd
sudo systemctl start libvirtd
sudo systemctl enable libvirtd
```

2. 检查连接 URI
```bash
# 测试连接
virsh -c qemu:///system list --all

# 检查 socket 文件
ls -la /run/libvirt/libvirt-sock
```

3. 检查用户权限
```bash
# 检查用户组
groups $USER

# 检查 socket 权限
ls -la /run/libvirt/
```

**解决方案：**

```bash
# 方案 1：使用 root 运行
sudo vm-analyzer-agent

# 方案 2：将用户添加到 libvirt 组
sudo usermod -aG libvirt $USER
# 重新登录生效

# 方案 3：检查 AppArmor/SELinux
sudo aa-status  # Ubuntu
getenforce      # CentOS/RHEL
```

---

### 问题：Redis 连接失败

**症状：**
```
ERROR: Redis connection failed
```

**排查步骤：**

1. 检查 Redis 服务
```bash
systemctl status redis
systemctl start redis
```

2. 测试 Redis 连接
```bash
redis-cli ping
# 应该返回 PONG
```

3. 检查 Redis 配置
```bash
redis-cli INFO server
redis-cli CONFIG GET bind
redis-cli CONFIG GET port
```

**解决方案：**

```python
# 检查 utils/config.py 中的配置
REDIS_DATABASE_CONFIG = {
    'host': 'localhost',  # 确保主机名正确
    'port': 6379,         # 确保端口正确
}
```

```bash
# 如果 Redis 有密码
redis-cli AUTH your_password
```

---

## 采集问题

### 问题：采集不到虚拟机指标

**症状：**
- 运行 agent 但无数据输出
- Redis 中没有 vm:* 键

**排查步骤：**

1. 检查虚拟机状态
```bash
virsh list --all
```

2. 检查 QEMU Guest Agent
```bash
# 在虚拟机内部检查
systemctl status qemu-guest-agent

# 在宿主机检查
virsh qemu-agent-command <vm-name> '{"execute":"guest-ping"}'
```

3. 检查 agent 通道
```bash
virsh dominfo <vm-name> | grep Agent
```

**解决方案：**

```bash
# 在虚拟机内安装 qemu-guest-agent
# CentOS/RHEL
sudo yum install -y qemu-guest-agent
sudo systemctl enable qemu-guest-agent
sudo systemctl start qemu-guest-agent

# Ubuntu/Debian
sudo apt-get install -y qemu-guest-agent
sudo systemctl enable qemu-guest-agent
sudo systemctl start qemu-guest-agent
```

4. 检查 XML 配置中的 channel
```xml
<channel type='unix'>
  <source mode='bind'/>
  <target type='virtio' name='org.qemu.guest_agent.0'/>
</channel>
```

---

### 问题：采集数据不完整

**症状：**
- 部分指标为 null 或 0
- 某些虚拟机有数据，其他没有

**排查步骤：**

1. 检查 agent 版本
```bash
# 在虚拟机内
qemu-ga --version
```

2. 启用调试模式
```bash
sudo vm-analyzer-agent -d
```

3. 检查权限
```bash
# 确保可以访问 /proc
ls -la /proc/
cat /proc/1/stat
```

**解决方案：**

```python
# 在 config.py 中调整采集间隔
VM_ANALYZERS_CONFIG = {
    'duration': 30  # 增加采集时长
}
```

---

## 性能问题

### 问题：采集器 CPU 占用过高

**症状：**
- vm-analyzer-agent 进程 CPU 使用率 > 10%
- 宿主机负载升高

**排查步骤：**

1. 检查采集间隔
```bash
# 当前设置
ps aux | grep vm-analyzer
```

2. 监控资源使用
```bash
top -p $(pgrep -d',' vm-analyzer)
```

**解决方案：**

```bash
# 增加采集间隔（建议生产环境 5-10 秒）
sudo vm-analyzer-agent -i 5

# 或者修改默认值
# 在 agent/main.py 中
interval = 5  # 默认 1 秒改为 5 秒
```

---

### 问题：Redis 内存占用过高

**症状：**
- Redis 内存持续增长
- 系统内存不足

**排查步骤：**

1. 检查 Redis 内存使用
```bash
redis-cli INFO memory
```

2. 检查键数量
```bash
redis-cli DBSIZE
redis-cli KEYS "vm:*" | wc -l
```

3. 检查数据过期策略
```bash
redis-cli TTL "vm:<uuid>"
```

**解决方案：**

```python
# 在 utils/config.py 中缩短保留时间
REDIS_RETENTION_SECONDS = 600  # 10 分钟

# 或者手动清理
redis-cli KEYS "vm:*" | xargs redis-cli DEL
```

---

## 权限问题

### 问题：Permission denied 访问虚拟机

**症状：**
```
error: failed to connect to the hypervisor
error: authentication failed
```

**排查步骤：**

1. 检查 polkit 规则
```bash
cat /etc/polkit-1/rules.d/50-libvirt.rules
```

2. 检查用户组成员
```bash
groups $USER
```

**解决方案：**

```bash
# 创建 polkit 规则
sudo tee /etc/polkit-1/rules.d/50-libvirt.rules << 'EOF'
polkit.addRule(function(action, subject) {
    if (action.id == "org.libvirt.unix.manage" &&
        subject.isInGroup("libvirt")) {
        return polkit.Result.YES;
    }
});
EOF

# 重启服务
sudo systemctl restart polkit
```

---

## 调试技巧

### 启用详细日志

```bash
# 调试模式
sudo vm-analyzer-agent -d

# 设置日志级别
export VM_ANALYZER_LOG_LEVEL=DEBUG
sudo -E vm-analyzer-agent
```

### 手动测试采集

```python
#!/usr/bin/env python
from agent.vm import VMFactory
from agent.storage import VMStatsRedisStorage
from agent.collector import VMStatsCollector

# 手动初始化
vm_factory = VMFactory('qemu:///system')
storage = VMStatsRedisStorage(vm_factory, 'cpuUsage')
ok, err = storage.check_connection()
print(f"Redis connection: {ok}, {err}")

collector = VMStatsCollector(vm_factory, storage, 'cpuUsage')
collector.record_stats()
print("Collection completed")
```

### 检查 Redis 数据

```bash
# 查看所有 VM 键
redis-cli KEYS "vm:*"

# 获取特定 VM 数据
redis-cli GET "vm:<uuid>"

# 监视实时数据
redis-cli MONITOR
```

---

## 获取帮助

如果以上方案无法解决问题：

1. 查看日志文件
```bash
journalctl -u vm-analyzer -f
```

2. 运行健康检查
```bash
python3 utils/health_check.py
```

3. 提交 Issue
- 包含系统信息：`uname -a`, `cat /etc/os-release`
- 包含版本信息：`vm-analyzer-agent -V`
- 包含错误日志
- 包含复现步骤
