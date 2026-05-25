---
title: "IDA+WSL2实现本地linux动态调试"
date: 2024-12-01 17:14:00
categories:
  - "CTF Writeup"
tags:
  - "CTF"
  - "Writeup"
  - "Pwn"
  - "Linux"
cnblogs_postid: "18580052"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18580052"
---

1、首先在ida安装目录找到dbgsrv这个文件夹，打开后把“linux_server”这个文件拖到你的linux中（我放在/root位置）
![image](/assets/cnblogs/IDA+WSL2实现本地linux动态调试/3539156-20241201170105763-852440625.png)
2、然后赋予两个文件权限（linux-server和要调试的文件）
```
chmod +x /root/linux_server
chmod +x 你的待调试文件位置
```
然后运行调试组件
```
/root/linux_server64
```
参数：
“-p端口”：用于设置备用TCP端口，以便服务器进行监听。默认端口是23946
“-P密码”：用于设置客户端连接调试服务器必需的密码，防止未授权连接。
“-v”：将服务器置于详细模式。
![image](/assets/cnblogs/IDA+WSL2实现本地linux动态调试/3539156-20241201170427852-1889226306.png)
然后打开ida，按F9选择调试器
![image](/assets/cnblogs/IDA+WSL2实现本地linux动态调试/3539156-20241201170610379-1757173351.png)
如果出现这个选择Yes
![image](/assets/cnblogs/IDA+WSL2实现本地linux动态调试/3539156-20241201170746577-453659385.png)
上面的前两个输文件所在linux的目录，第三个输文件路径，下面填上终端显示的my ip，密码为linux账号的密码
![image](/assets/cnblogs/IDA+WSL2实现本地linux动态调试/3539156-20241201171056477-1520020619.png)
![image](/assets/cnblogs/IDA+WSL2实现本地linux动态调试/3539156-20241201171242713-756137646.png)
（当然，如果懒得移动文件，ida也可以把文件自动导入到linux中，只需要路径不正确就行）
如果配置都没有问题，接下来应该就会进入动态调试界面了
![image](/assets/cnblogs/IDA+WSL2实现本地linux动态调试/3539156-20241201171314478-671391004.png)
![image](/assets/cnblogs/IDA+WSL2实现本地linux动态调试/3539156-20241201171503342-1179287691.png)
