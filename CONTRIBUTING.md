# 贡献指南

欢迎参与 VMAnalyzer 项目贡献！以下是贡献指南：

## 开发流程

1. Fork 本仓库到自己的账号
2. 克隆你的 fork 到本地：`git clone https://gitcode.com/[你的账号]/VMAnalyzer.git`
3. 切换到 develope-251121 分支：`git checkout develope-251121`
4. 创建新的功能分支：`git checkout -b feat/[功能名称]` 或 `git checkout -b fix/[修复描述]`
5. 进行代码修改
6. 提交代码：`git commit -m "[类型]: [描述]"`，类型包括：feat/fix/docs/style/refactor/test/chore
7. 推送分支到你的 fork：`git push origin [分支名称]`
8. 提交 Pull Request 到上游仓库的 develope-251121 分支

## 代码规范

* 遵循 PEP 8 代码规范
* 函数和方法需要有 docstring 注释
* 所有新功能必须包含单元测试
* 提交前确保所有测试通过：`pytest tests/`
* 提交信息遵循约定式提交规范

## 提交规范

提交信息格式：
```
<类型>(<范围>): <主题>

<正文>

<页脚>
```

类型：
* feat: 新功能
* fix: 修复bug
* docs: 文档修改
* style: 代码格式修改
* refactor: 代码重构
* test: 测试相关修改
* chore: 构建/工具等辅助工具的变动

## 报告问题

* 提交 Issue 前请先搜索是否已有相关问题
* 详细描述问题的复现步骤
* 提供系统环境、Python版本、libvirt版本等信息
* 如果可以，提供错误日志和堆栈信息

感谢你的贡献！
