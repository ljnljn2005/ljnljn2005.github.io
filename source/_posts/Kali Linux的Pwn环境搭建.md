---
title: "Kali Linux的Pwn环境搭建"
date: 2024-11-28 21:38:00
categories:
  - "CTF Writeup"
tags:
  - "CTF"
  - "Writeup"
  - "Pwn"
  - "Linux"
cnblogs_postid: "18575303"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18575303"
---

链接指北：
1、安装pwntools、gdb等插件
参考链接：https://blog.csdn.net/Bossfrank/article/details/130213456
2、途中出现以下问题解决方案
链接：https://blog.csdn.net/2202_75762088/article/details/134625775#/
```
error: externally-managed-environment
 
× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.
    
    If you wish to install a non-Debian-packaged Python package,
    create a virtual environment using python3 -m venv path/to/venv.
    Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make
    sure you have python3-full installed.
    
    If you wish to install a non-Debian packaged Python application,
    it may be easiest to use pipx install xyz, which will manage a
    virtual environment for you. Make sure you have pipx installed.
    
    See /usr/share/doc/python3.11/README.venv for more information.
 
note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
hint: See PEP 668 for the detailed specification.
```
3、简易快速入门
链接：https://blog.csdn.net/weixin_45004513/article/details/117332121
导入Pwntools
```
from pwn import *
```
链接
```
r = remote("目标地址str类型", 目标端口int类型)#与服务器交互
r = process("目标程序位置")#与本地程序交互
```
构造payload之打包
```
p64(int)#将int类型打包成64位存储
p32(int)#将int类型打包成32位存储
```
发送
```
r.sendline(playload)#发送playload为一行（自动在尾部加上\n）
```
接收
```
r.recv()#接收到结束
r.recvuntil(end, drop=True)end(str)#接受到end之后截至，drop=True时不包括end，drop=False时包括end
```
打开交互
```
r.interactive()#一般在末尾都要加
```
