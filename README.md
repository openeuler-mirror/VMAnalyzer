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

欢迎参与VMAnalyzer项目贡献！详细贡献指南请参考 [CONTRIBUTING.md](CONTRIBUTING.md) 文件。

基本贡献流程：
1.  Fork 本仓库到自己的账号
2.  克隆 fork 到本地：`git clone https://gitcode.com/[你的账号]/VMAnalyzer.git`
3.  切换到开发分支：`git checkout develope-251121`
4.  创建功能分支：`git checkout -b feat/[功能名称]` 或 `git checkout -b fix/[修复描述]`
5.  进行代码修改，确保符合代码规范
6.  提交代码：`git commit -m "[类型]: [描述]"`
7.  推送分支到你的 fork：`git push origin [分支名称]`
8.  提交 Pull Request 到上游仓库的 `develope-251121` 分支

提交代码前请确保：
- 所有单元测试通过：`pytest tests/unit/`
- 代码符合PEP 8规范
- 提交信息遵循约定式提交规范

#### 文档资源

- [架构设计文档](ARCHITECTURE.md)
- [安装指南](INSTALL.md)
- [使用示例](USAGE.md)
- [常见问题](FAQ.md)
- [项目路线图](ROADMAP.md)


#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  AtomGit 官方博客 [blog.atomgit.com](https://blog.atomgit.com)
3.  你可以 [https://atomgit.com/explore](https://atomgit.com/explore) 这个地址来了解 AtomGit 上的优秀开源项目
4.  [GVP](https://atomgit.com/gvp) 全称是 AtomGit 最有价值开源项目，是综合评定出的优秀开源项目
5.  AtomGit 官方提供的使用手册 [https://atomgit.com/help](https://atomgit.com/help)
6.  AtomGit 封面人物是一档用来展示 AtomGit 会员风采的栏目 [https://atomgit.com/atomgit-stars/](https://atomgit.com/atomgit-stars/)
