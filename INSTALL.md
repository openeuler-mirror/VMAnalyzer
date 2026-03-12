# 安装指南

## 环境要求

### 操作系统
- openEuler 20.03 LTS SP3 及以上版本
- CentOS 8 及以上版本
- Ubuntu 20.04 及以上版本
- Debian 11 及以上版本

### 依赖软件
- Python 3.6 及以上版本
- libvirt 6.0 及以上版本
- Redis 5.0 及以上版本
- python3-libvirt
- gcc、python3-devel、libvirt-devel（编译依赖）

## 安装方式

### 方式一：源码安装
```bash
# 1. 安装系统依赖
yum install -y python3 python3-pip python3-libvirt gcc python3-devel libvirt-devel redis

# 2. 启动Redis服务
systemctl start redis
systemctl enable redis

# 3. 下载源码
git clone https://gitee.com/openeuler/VMAnalyzer.git
cd VMAnalyzer

# 4. 安装Python依赖
pip3 install -r requirements.txt

# 5. 安装VMAnalyzer
pip3 install -e .

# 6. 验证安装
vm-analyzer-agent --help
```

### 方式二：容器化部署
```bash
# 1. 安装Docker和Docker Compose
yum install -y docker docker-compose
systemctl start docker
systemctl enable docker

# 2. 下载源码
git clone https://gitee.com/openeuler/VMAnalyzer.git
cd VMAnalyzer

# 3. 启动服务
docker-compose up -d

# 4. 查看运行状态
docker-compose ps
```

### 方式三：RPM包安装
```bash
# 1. 配置openEuler软件源
yum install -y VMAnalyzer
```

## 验证安装
```bash
# 查看版本
vm-analyzer-agent -V

# 测试运行
sudo vm-analyzer-agent -d -t 10
```

## 配置说明
```bash
# 复制配置模板
cp config.example.py config.py

# 编辑配置文件，根据需要修改参数
vim config.py
```

## 卸载
```bash
# 源码安装卸载
pip3 uninstall -y VMAnalyzer

# 容器化卸载
docker-compose down -v

# RPM包卸载
yum remove -y VMAnalyzer
```

## 常见安装问题排查
### 问题1：安装时提示Python版本过低
```
Python版本需要3.6及以上，可通过以下命令查看版本：
```bash
python3 --version
```
### 问题2：运行时提示权限不足
请使用root用户运行，或者将当前用户加入libvirt组：
```bash
usermod -aG libvirt your_username
```
### 问题3：Redis连接失败
请检查Redis服务是否正常运行，配置文件中的Redis地址和端口是否正确。
