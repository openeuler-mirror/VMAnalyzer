# 常见问题 FAQ

## 安装相关问题

### Q: 安装时提示找不到python3-libvirt包怎么办？
A: 请先安装epel源，然后再安装：
```bash
yum install -y epel-release
yum install -y python3-libvirt
```

### Q: 运行时提示"Failed to connect to QEMU/KVM"怎么办？
A: 请检查：
1. libvirtd服务是否运行：`systemctl status libvirtd`
2. 当前用户是否有libvirt访问权限，建议使用root运行或加入libvirt组
3. libvirt连接URI是否正确

### Q: 采集不到虚拟机指标怎么办？
A: 请检查：
1. 虚拟机是否处于运行状态
2. 虚拟机是否安装了qemu-guest-agent
3. qemu-guest-agent服务是否在虚拟机内运行
4. libvirt是否开启了qemu-agent通道

## 使用相关问题

### Q: 如何自定义采集间隔？
A: 使用 `-i` 参数指定采集间隔（秒）：
```bash
vm-analyzer-agent -i 10  # 每10秒采集一次
```

### Q: 数据存储在哪里？
A: 默认存储在本地Redis数据库中，数据保留时间为1小时，可以在配置文件中修改。

### Q: 如何查看历史数据？
A: 可以通过Redis客户端查询：
```bash
redis-cli keys "vm:*"
redis-cli get "vm:<uuid>"
```

### Q: 支持哪些类型的虚拟机？
A: 目前主要支持KVM/QEMU类型的虚拟机，基于libvirt进行管理。

## 性能相关问题

### Q: 采集器对宿主机性能影响大吗？
A: 影响非常小，默认采集间隔为1秒时，CPU使用率通常小于1%，内存占用小于50MB。

### Q: 最多支持同时监控多少台虚拟机？
A: 单实例默认支持同时监控100台以内的虚拟机，超过的话建议适当调大采集间隔。

## 告警相关问题

### Q: 如何配置告警阈值？
A: 复制config.example.py为config.py，修改其中的ALERT_THRESHOLDS配置项。

### Q: 支持哪些告警方式？
A: 目前支持日志告警，后续会支持邮件、Webhook、短信等告警方式。

## 开发相关问题

### Q: 如何添加新的采集指标？
A: 在gather目录下添加新的采集脚本，遵循现有脚本的编码规范即可。

### Q: 如何贡献代码？
A: 请参考CONTRIBUTING.md文件中的贡献指南。

### Q: 如何优化Redis内存使用？
A: 可以通过以下方式优化：
1. 调整maxmemory配置限制内存使用
2. 设置合理的键过期时间
3. 定期清理过期数据
4. 使用Redis持久化配置

### Q: 采集间隔设置多少合适？
A: 根据实际需求：
- 实时监控：1-5秒
- 常规监控：10-30秒
- 历史分析：60秒以上
