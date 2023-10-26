# VMAnalyzer

#### Description
A lightweight virtualization performance monitoring analysis tool

#### Installation

1.  Install dependency packages
   ```
   $ yum install -y python3-libvirt
   ```

2.  Go to the project directory and install it using the pip command
   ```
   $ cd bstperf
   $ sudo pip3 install -e .
   ```

#### Instructions

1.  View help
   ```
   $ vm-analyzer-agent --help
   usage: vm-analyzer-agent [-hdi] [uri]
      uri will default to qemu:///system
      --help, -h   Print this help message
      --debug, -d  Print debug output
      --interval=SECS, -i  Configure statistics collection interval
      --timeout=SECS, -t  Quit after SECS seconds running
   ```

2.  Execute the vm-Analyser-Agent program
   ```
   # vm-analyzer-agent
   ```

3.  Enable debug mode
   ```
   # vm-analyzer-agent -d
   ```

#### Contribution

1.  Fork the repository
2.  Create Feat_xxx branch
3.  Commit your code
4.  Create Pull Request


#### Gitee Feature

1.  You can use Readme\_XXX.md to support different languages, such as Readme\_en.md, Readme\_zh.md
2.  Gitee blog [blog.gitee.com](https://blog.gitee.com)
3.  Explore open source project [https://gitee.com/explore](https://gitee.com/explore)
4.  The most valuable open source project [GVP](https://gitee.com/gvp)
5.  The manual of Gitee [https://gitee.com/help](https://gitee.com/help)
6.  The most popular members  [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
