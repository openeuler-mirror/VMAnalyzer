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


#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  AtomGit 官方博客 [blog.atomgit.com](https://blog.atomgit.com)
3.  你可以 [https://atomgit.com/explore](https://atomgit.com/explore) 这个地址来了解 AtomGit 上的优秀开源项目
4.  [GVP](https://atomgit.com/gvp) 全称是 AtomGit 最有价值开源项目，是综合评定出的优秀开源项目
5.  AtomGit 官方提供的使用手册 [https://atomgit.com/help](https://atomgit.com/help)
6.  AtomGit 封面人物是一档用来展示 AtomGit 会员风采的栏目 [https://atomgit.com/atomgit-stars/](https://atomgit.com/atomgit-stars/)
