# 使用示例

## 快速开始

### 1. 基本运行
```bash
# 默认方式运行，采集所有虚拟机指标
sudo vm-analyzer-agent

# 指定libvirt连接URI
sudo vm-analyzer-agent qemu+ssh://root@192.168.1.100/system
```

### 2. 常用参数

#### 设置采集间隔
```bash
# 每5秒采集一次指标
sudo vm-analyzer-agent -i 5
```

#### 运行指定时间后退出
```bash
# 运行300秒（5分钟）后自动退出
sudo vm-analyzer-agent -t 300
```

#### 调试模式
```bash
# 开启调试日志输出
sudo vm-analyzer-agent -d
```

#### 输出指标到文件
```bash
# 将分析结果保存到JSON文件
sudo vm-analyzer-agent -o /var/log/vm_metrics.jsonl
```

#### 查看版本
```bash
vm-analyzer-agent -V
```

### 3. 指标采集模式

#### 监控CPU使用率
```bash
sudo vm-analyzer-agent
```

#### 监控内存使用率
```bash
sudo vm-analyzer-agent -m
```

#### 监控网络流量
```bash
sudo vm-analyzer-agent -n
```

#### 监控磁盘IO
```bash
sudo vm-analyzer-agent -b
```

#### 监控vCPU状态和亲和性
```bash
sudo vm-analyzer-agent -v
```

#### 监控进程资源使用
```bash
sudo vm-analyzer-agent -p
```

### 4. 高级用法

#### 结合Redis持久化存储
确保Redis服务已启动，默认配置会自动连接本地Redis：
```bash
sudo systemctl start redis
sudo vm-analyzer-agent
```

#### 自定义告警阈值
复制配置模板并修改阈值：
```bash
cp config.example.py config.py
# 编辑config.py修改ALERT_THRESHOLDS配置
```

#### 容器化部署
```bash
# 使用docker-compose部署
docker-compose up -d

# 查看运行日志
docker-compose logs -f vm-analyzer
```

### 5. 查看采集的数据
```python
import redis
import json

r = redis.Redis()
keys = r.keys("vm:*")
for key in keys:
    data = json.loads(r.get(key))
    print(f"VM {key.decode()}: CPU={data['cpu_usage']}% Memory={data['memory_usage']}%")
```
