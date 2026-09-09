简体中文 | [English](./README.en.md) 

# VMAnalyzer

#### 介绍
A lightweight virtualization performance monitoring analysis tool

#### 安装教程

1.  安装依赖包
   ```
   $ yum install -y python3-libvirt
   ```

2.  进入工程目录，通过pip命令安装
   ```
   $ cd VMAnalyzer
   $ sudo pip3 install -e .
   ```

#### 使用说明

1.  查看帮助
   ```
   $ vm-analyzer-agent --help
   usage: vm-analyzer-agent [-hdi] [uri]
      uri will default to qemu:///system
      --help, -h   Print this help message
      --debug, -d  Print debug output
      --interval=SECS, -i  Configure statistics collection interval
      --timeout=SECS, -t  Quit after SECS seconds running
   ```

2.  执行vm-analyzer-agent程序
   ```
   # vm-analyzer-agent
   ```

3.  开启调试模式
   ```
   # vm-analyzer-agent -d
   ```

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


