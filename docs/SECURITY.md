# 安全最佳实践指南

本文档提供 VMAnalyzer 的安全配置建议，帮助您在生产环境中安全地部署和运行。

## 目录

- [概述](#概述)
- [运行权限](#运行权限)
- [网络安全](#网络安全)
- [Redis 安全](#redis-安全)
- [数据保护](#数据保护)
- [审计日志](#审计日志)
- [容器安全](#容器安全)

---

## 概述

VMAnalyzer 需要访问敏感的虚拟化基础设施，因此安全配置至关重要。

### 安全原则

| 原则 | 说明 |
|------|------|
| 最小权限 | 只授予必要的权限 |
| 纵深防御 | 多层安全控制 |
| 安全默认 | 默认配置即安全 |
| 审计追踪 | 记录所有关键操作 |

---

## 运行权限

### 推荐：专用用户运行

```bash
# 创建专用用户
sudo useradd -r -s /bin/false vmanalyzer

# 添加到 libvirt 组
sudo usermod -aG libvirt vmanalyzer

# 设置文件权限
sudo chown -R vmanalyzer:vmanalyzer /opt/vmanalyzer
sudo chmod 750 /opt/vmanalyzer
```

### Systemd 服务配置

```ini
# /etc/systemd/system/vm-analyzer.service
[Unit]
Description=VM Analyzer Agent
After=network.target redis.service

[Service]
Type=simple
User=vmanalyzer
Group=vmanalyzer
ExecStart=/opt/vmanalyzer/venv/bin/vm-analyzer-agent
Restart=always

# 安全加固
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/lib/vmanalyzer

[Install]
WantedBy=multi-user.target
```

### 避免 root 运行的风险

**风险：**
- 代码漏洞可能导致系统被入侵
- 配置错误可能破坏虚拟化环境
- 日志注入可能执行恶意命令

**缓解措施：**
```bash
# 使用 capabilities 而非 root
sudo setcap cap_sys_admin,cap_sys_ptrace+eip /usr/bin/vm-analyzer-agent

# 或者使用 sudoers 限制命令
# /etc/sudoers.d/vmanalyzer
vmanalyzer ALL=(root) NOPASSWD: /usr/bin/vm-analyzer-agent
```

---

## 网络安全

### libvirt 连接安全

```bash
# 使用 TLS 连接远程 libvirt
# /etc/libvirt/libvirtd.conf

# 启用 TLS
listen_tls = 1
tls_port = "16514"

# 证书配置
tls_allowed_dn_list = ["CN=vmanalyzer"]
```

```python
# VMAnalyzer 配置
LIBVIRT_URI = "qemu+tls://vmanalyzer@remote-host/system"
```

### 防火墙配置

```bash
# 仅允许必要的连接

# 本地 Redis（如果不需要远程访问）
iptables -A INPUT -p tcp --dport 6379 -s 127.0.0.1 -j ACCEPT
iptables -A INPUT -p tcp --dport 6379 -j DROP

# libvirt TLS
iptables -A INPUT -p tcp --dport 16514 -s TRUSTED_IP -j ACCEPT
iptables -A INPUT -p tcp --dport 16514 -j DROP
```

---

## Redis 安全

### 启用认证

```bash
# /etc/redis/redis.conf

# 设置强密码
requirepass YourStrongPasswordHere

# 禁用危险命令
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command CONFIG "CONFIG_9f3b2a1e"

# 绑定到特定接口
bind 127.0.0.1

# 启用保护模式
protected-mode yes
```

```python
# utils/config.py
REDIS_DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 6379,
    'password': 'YourStrongPasswordHere',  # 从环境变量读取更安全
    'socket_timeout': 5,
}
```

### 使用 Unix Socket（推荐）

```bash
# /etc/redis/redis.conf
port 0
unixsocket /var/run/redis/redis.sock
unixsocketperm 770
```

```python
REDIS_DATABASE_CONFIG = {
    'unix_socket_path': '/var/run/redis/redis.sock'
}
```

### 数据加密

```python
# 敏感数据加密存储
from cryptography.fernet import Fernet

class EncryptedStorage:
    def __init__(self, key):
        self.cipher = Fernet(key)
    
    def save_encrypted(self, redis_client, key, data):
        encrypted = self.cipher.encrypt(json.dumps(data).encode())
        redis_client.set(key, encrypted)
    
    def get_decrypted(self, redis_client, key):
        encrypted = redis_client.get(key)
        if encrypted:
            return json.loads(self.cipher.decrypt(encrypted))
        return None
```

---

## 数据保护

### 敏感数据处理

```python
# 避免在日志中记录敏感信息
import logging

class SensitiveFilter(logging.Filter):
    def filter(self, record):
        # 过滤密码、密钥等
        record.msg = str(record.msg).replace('password=', 'password=***')
        return True

logger.addFilter(SensitiveFilter())
```

### 数据保留策略

```python
# utils/config.py

# 缩短数据保留时间
REDIS_RETENTION_SECONDS = 1800  # 30 分钟

# 启用数据清理
def cleanup_sensitive_data(redis_client):
    """定期清理可能包含敏感信息的数据"""
    keys = redis_client.keys('vm:*:processes')
    for key in keys:
        # 清理进程列表中的命令行参数
        data = redis_client.get(key)
        if data:
            cleaned = sanitize_process_data(json.loads(data))
            redis_client.set(key, json.dumps(cleaned))
```

---

## 审计日志

### 启用审计

```python
# utils/audit_logger.py

import logging
import json
from datetime import datetime

audit_logger = logging.getLogger('vmanalyzer.audit')

class AuditLogger:
    @staticmethod
    def log_action(action, user, resource, details=None):
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'action': action,
            'user': user,
            'resource': resource,
            'details': details or {}
        }
        audit_logger.info(json.dumps(entry))
    
    @staticmethod
    def log_vm_access(vm_uuid, vm_name, operation):
        AuditLogger.log_action(
            action='VM_ACCESS',
            user='vmanalyzer',
            resource=f'vm:{vm_uuid}',
            details={'vm_name': vm_name, 'operation': operation}
        )
```

### 审计事件

| 事件类型 | 说明 |
|----------|------|
| VM_ACCESS | 访问虚拟机信息 |
| METRIC_COLLECT | 采集指标数据 |
| CONFIG_CHANGE | 配置变更 |
| ALERT_TRIGGER | 告警触发 |
| LOGIN_ATTEMPT | 登录尝试 |

---

## 容器安全

### Dockerfile 安全

```dockerfile
# 使用官方基础镜像
FROM python:3.9-slim

# 创建非 root 用户
RUN groupadd -r vmanalyzer && useradd -r -g vmanalyzer vmanalyzer

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . /app
WORKDIR /app
RUN chown -R vmanalyzer:vmanalyzer /app

# 切换到非 root 用户
USER vmanalyzer

# 只读文件系统
VOLUME ["/tmp"]

ENTRYPOINT ["vm-analyzer-agent"]
```

### Docker Compose 安全

```yaml
version: '3'

services:
  vmanalyzer:
    build: .
    user: "1000:1000"
    read_only: true
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - SYS_PTRACE
      - SYS_ADMIN
    tmpfs:
      - /tmp:noexec,nosuid,size=100m
    volumes:
      - ./config.py:/app/config.py:ro
      - /run/libvirt:/run/libvirt:ro
```

### Kubernetes 安全

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vmanalyzer
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
      - name: vmanalyzer
        image: vmanalyzer:latest
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
            add:
            - SYS_PTRACE
        resources:
          limits:
            memory: "256Mi"
            cpu: "500m"
          requests:
            memory: "128Mi"
            cpu: "250m"
```

---

## 安全 checklist

### 部署前检查

- [ ] 使用专用用户运行，非 root
- [ ] Redis 已启用认证
- [ ] libvirt 连接使用 TLS（远程场景）
- [ ] 防火墙限制访问来源
- [ ] 敏感配置从环境变量或密钥管理服务读取
- [ ] 审计日志已启用
- [ ] 数据保留策略已配置
- [ ] 容器以只读模式运行

### 定期审查

- [ ] 检查日志中的异常访问
- [ ] 审查 Redis 中的敏感数据
- [ ] 更新依赖包到最新版本
- [ ] 轮换认证凭证
- [ ] 验证备份加密

---

## 应急响应

### 安全事件处理

1. **立即隔离**
   ```bash
   systemctl stop vm-analyzer
   iptables -A OUTPUT -p tcp --dport 6379 -j DROP
   ```

2. **保留证据**
   ```bash
   cp /var/log/vmanalyzer/*.log /secure/evidence/
   redis-cli SAVE
   cp /var/lib/redis/dump.rdb /secure/evidence/
   ```

3. **分析影响**
   - 检查日志中的未授权访问
   - 验证 VM 完整性
   - 检查配置是否被篡改

4. **恢复服务**
   - 修复漏洞
   - 轮换所有凭证
   - 逐步恢复服务
