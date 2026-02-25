### 功能说明
宿主机/虚机健康检查

### 配置
##默认对比的配置文件在/usr/bin/vm_analyer/diagnose/virt_check下，详细如下：
类别   配置文件	                           使用途径	                 节点
高级版 premium-config-libvirtd.conf	   虚拟化libvirt配置	         宿主机
高级版 premium-config-qemu.conf	           虚机化qemu.conf配置	         宿主机
高级版 premium-config-sysctl.conf	   内核调优配置	                 宿主机
高级版 premium-config-sysctl-libvirt.conf  虚拟化sysctl-libvirt配置      宿主机
高级版 premium-config.env	           除了上面四个配置以外的配置	 宿主机/虚拟机
