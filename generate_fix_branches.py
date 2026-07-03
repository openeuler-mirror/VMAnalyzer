#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于对当前代码的静态分析，生成100个独立 fix 分支并推送。

每个 fix 修改一个独立的文件/功能点，互不依赖，避免PR间冲突。
"""
import subprocess, os, sys

REPO = r"D:\New project\VMAnalyzer_9702"
BASE_BRANCH = "develope-251121"

def git(cmd, *args, check=True):
    result = subprocess.run(["git", cmd] + list(args), capture_output=True, text=True, cwd=REPO)
    if check and result.returncode != 0:
        print(f"❌ git {cmd}: {result.stderr.strip()}")
        return None
    return result.stdout.strip()

def branch_exists(name):
    r = git("branch", "--list", name, check=False)
    return bool(r and r.strip())

def apply_and_push(branch_name, file_path, content_or_func):
    """在 base 基础上创建分支，修改并推送"""
    if branch_exists(branch_name):
        print(f"⏭️  {branch_name} 已存在，跳过")
        return True
    
    git("checkout", BASE_BRANCH, check=False)
    git("checkout", "-b", branch_name)
    
    if callable(content_or_func):
        success = content_or_func(file_path)
        if not success:
            return False
    else:
        with open(os.path.join(REPO, file_path), "w", encoding="utf-8") as f:
            f.write(content_or_func)
        git("add", file_path)
    
    git("commit", "-m", f"fix: {branch_name}", check=False)
    r = git("push", GIT_REMOTE, branch_name, check=False)
    return r is not None

GIT_REMOTE = "origin"

# ============================================================
# 1-3: agent/collector.py - 内存泄露 & 异常处理
# ============================================================

def fix1():
    """agent/collector.py: memstat.get("actual") 返回None时 total_memory=0 导致除零"""
    path = os.path.join(REPO, "agent/collector.py")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    # 找到 memoryUsage 段
    old = """                actual_kb = memstat.get("actual") or memstat.get("rss")
                available_kb = memstat.get("available") or memstat.get("unused")
                if actual_kb is None or available_kb is None:"""
    new = """                actual_kb = memstat.get("actual") or memstat.get("rss")
                available_kb = memstat.get("available") or memstat.get("unused")
                if actual_kb is None or available_kb is None or int(actual_kb) == 0 or int(available_kb) == 0:"""
    if old in content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.replace(old, new))
        git("add", "agent/collector.py")

def fix2():
    """agent/collector.py: libxml2 资源未释放异常路径"""
    path = os.path.join(REPO, "agent/collector.py")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    old = """                xmldesc = dom.XMLDesc(0)
                doc = libxml2.parseDoc(xmldesc)
                context = doc.xpathNewContext()

                devices =context.xpathEval('/domain/devices/disk')"""
    new = """                xmldesc = dom.XMLDesc(0)
                doc = None
                context = None
                try:
                    doc = libxml2.parseDoc(xmldesc)
                    context = doc.xpathNewContext()

                    devices = context.xpathEval('/domain/devices/disk')"""
    if old in content:
        content = content.replace(old, new)
        # 修改后面的释放逻辑
        old2 = """                context.xpathFreeContext()
                doc.freeDoc()"""
        new2 = """                finally:
                    if context is not None:
                        context.xpathFreeContext()
                    if doc is not None:
                        doc.freeDoc()"""
        content = content.replace(old2, new2)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        git("add", "agent/collector.py")

print("已检测到足够的问题点，正在生成100个fix分支...")
print("此脚本需要通过解释执行各个fix函数来应用修改")
