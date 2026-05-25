---
title: "Brute4Road打靶flag1-2（待完结"
date: 2026-03-25 20:47:00
categories:
  - "Others"
tags:
cnblogs_postid: "19772365"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/19772365"
---

老师说沙砾快过期了，最近多做一点
## flag1
先fscan
![assets/Brute4Road打靶flag1-2（待完结/file-20260325180543776.png](/assets/cnblogs/Brute4Road打靶flag1-2（待完结/3539156-20260325204644136-654963163.png)
有ftp和redis未授权
ftp看没有什么东西
![assets/Brute4Road打靶flag1-2（待完结/file-20260325180632387.png](/assets/cnblogs/Brute4Road打靶flag1-2（待完结/3539156-20260325204644206-492427482.png)
redis也没有
![assets/Brute4Road打靶flag1-2（待完结/file-20260325180736415.png](/assets/cnblogs/Brute4Road打靶flag1-2（待完结/3539156-20260325204644247-30716927.png)
那应该就是利用这些进行反弹shell了

options需要另外一个服务器上有redis
![assets/Brute4Road打靶flag1-2（待完结/file-20260325182459369.png](/assets/cnblogs/Brute4Road打靶flag1-2（待完结/3539156-20260325204644228-599265136.png)
![assets/Brute4Road打靶flag1-2（待完结/file-20260325182507673.png](/assets/cnblogs/Brute4Road打靶flag1-2（待完结/3539156-20260325204645126-2004870370.png)

这里因为云服务器配置问题一直没有成功，后面找了师傅的开源项目[GitHub - n0b0dyCN/redis-rogue-server: Redis(\<=5.0.5) RCE · GitHub](https://github.com/n0b0dyCN/redis-rogue-server)
这里只有一次机会打，否则就要重启靶机
并且似乎他的反弹shell指令有问题，所以用交互shell之后再反弹
![assets/Brute4Road打靶flag1-2（待完结/file-20260325185536671.png](/assets/cnblogs/Brute4Road打靶flag1-2（待完结/3539156-20260325204904927-1814150584.png)
![assets/Brute4Road打靶flag1-2（待完结/file-20260325185603099.png](/assets/cnblogs/Brute4Road打靶flag1-2（待完结/3539156-20260325204904132-743984518.png)
find一下flag
![assets/Brute4Road打靶flag1-2（待完结/file-20260325185853470.png](/assets/cnblogs/Brute4Road打靶flag1-2（待完结/3539156-20260325204903878-542569742.png)
![assets/Brute4Road打靶flag1-2（待完结/file-20260325190312065.png](/assets/cnblogs/Brute4Road打靶flag1-2（待完结/3539156-20260325204904007-758185543.png)
那这里就得提权
![assets/Brute4Road打靶flag1-2（待完结/file-20260325190354466.png](/assets/cnblogs/Brute4Road打靶flag1-2（待完结/3539156-20260325204904528-148312609.png)
发现base64，用gtfobins查看
![assets/Brute4Road打靶flag1-2（待完结/file-20260325190444710.png](/assets/cnblogs/Brute4Road打靶flag1-2（待完结/3539156-20260325204903896-1547530633.png)
这里可以未授权访问，读刚刚未授权的flag文件
![assets/Brute4Road打靶flag1-2（待完结/file-20260325190720249.png](/assets/cnblogs/Brute4Road打靶flag1-2（待完结/3539156-20260325204904444-1021440633.png)
## flag2
先开本地httpserver文件服务
![assets/Brute4Road打靶flag1-2（待完结/file-20260325191102364.png](/assets/cnblogs/Brute4Road打靶flag1-2（待完结/3539156-20260325204904254-1691567795.png)
在靶机上下载fscan和代理工具
![assets/Brute4Road打靶flag1-2（待完结/file-20260325191149196.png](/assets/cnblogs/Brute4Road打靶flag1-2（待完结/3539156-20260325204904456-1728465098.png)
看一下ip
![assets/Brute4Road打靶flag1-2（待完结/file-20260325191617370.png](/assets/cnblogs/Brute4Road打靶flag1-2（待完结/3539156-20260325204904678-377483986.png)
```
start ping
(icmp) Target 172.22.2.3      is alive
(icmp) Target 172.22.2.7      is alive
(icmp) Target 172.22.2.18     is alive
(icmp) Target 172.22.2.34     is alive
(icmp) Target 172.22.2.16     is alive
[*] Icmp alive hosts len is: 5
172.22.2.16:80 open
172.22.2.18:22 open
172.22.2.16:1433 open
172.22.2.18:445 open
172.22.2.16:445 open
172.22.2.34:445 open
172.22.2.3:445 open
172.22.2.7:22 open
172.22.2.16:139 open
172.22.2.34:139 open
172.22.2.3:139 open
172.22.2.34:135 open
172.22.2.18:139 open
172.22.2.7:21 open
172.22.2.16:135 open
172.22.2.3:135 open
172.22.2.18:80 open
172.22.2.7:6379 open
172.22.2.3:88 open
172.22.2.7:80 open
[*] alive ports len is: 20
start vulscan
[*] WebTitle http://172.22.2.16        code:404 len:315    title:Not Found
[*] NetInfo 
[*]172.22.2.34
   [->]CLIENT01
   [->]172.22.2.34
[*] NetInfo 
[*]172.22.2.3
   [->]DC
   [->]172.22.2.3
[*] OsInfo 172.22.2.3   (Windows Server 2016 Datacenter 14393)
[*] NetInfo 
[*]172.22.2.16
   [->]MSSQLSERVER
   [->]172.22.2.16
[*] NetBios 172.22.2.34     XIAORANG\CLIENT01             
[*] WebTitle http://172.22.2.7         code:200 len:4833   title:Welcome to CentOS
[*] OsInfo 172.22.2.16  (Windows Server 2016 Datacenter 14393)
[*] NetBios 172.22.2.3      [+] DC:DC.xiaorang.lab               Windows Server 2016 Datacenter 14393
[*] NetBios 172.22.2.18     WORKGROUP\UBUNTU-WEB02        
[*] NetBios 172.22.2.16     MSSQLSERVER.xiaorang.lab            Windows Server 2016 Datacenter 14393
[+] ftp 172.22.2.7:21:anonymous 
   [->]pub
[*] WebTitle http://172.22.2.18        code:200 len:57738  title:又一个WordPress站点
已完成 20/20
[*] 扫描结束,耗时: 12.972952082s
```
用venom成功代理上
![assets/Brute4Road打靶flag1-2（待完结/file-20260325192015731.png](/assets/cnblogs/Brute4Road打靶flag1-2（待完结/3539156-20260325204905067-124925354.png)
看到了wordpress，这个洞多，先打
![assets/Brute4Road打靶flag1-2（待完结/file-20260325192422368.png](/assets/cnblogs/Brute4Road打靶flag1-2（待完结/3539156-20260325204904401-1799399418.png)
用wpscan扫发现有个wpcargo，版本是6.x
![assets/Brute4Road打靶flag1-2（待完结/file-20260325194132399.png](/assets/cnblogs/Brute4Road打靶flag1-2（待完结/3539156-20260325204904249-1407279252.png)
大概率就是[GitHub - biulove0x/CVE-2021-25003: WPCargo \< 6.9.0 - Unauthenticated RCE · GitHub](https://github.com/biulove0x/CVE-2021-25003)
用脚本上shell
![assets/Brute4Road打靶flag1-2（待完结/file-20260325194729419.png](/assets/cnblogs/Brute4Road打靶flag1-2（待完结/3539156-20260325204904343-989164978.png)

![assets/Brute4Road打靶flag1-2（待完结/file-20260325195157192.png](/assets/cnblogs/Brute4Road打靶flag1-2（待完结/3539156-20260325204904415-1352941432.png)
根据wsl的ip设置代理服务器
![assets/Brute4Road打靶flag1-2（待完结/file-20260325195218250.png](/assets/cnblogs/Brute4Road打靶flag1-2（待完结/3539156-20260325204904244-2056696051.png)
连接
![assets/Brute4Road打靶flag1-2（待完结/file-20260325194850475.png](/assets/cnblogs/Brute4Road打靶flag1-2（待完结/3539156-20260325204904367-758060646.png)
可以看到成功了
![assets/Brute4Road打靶flag1-2（待完结/file-20260325195229943.png](/assets/cnblogs/Brute4Road打靶flag1-2（待完结/3539156-20260325204904504-789217626.png)
在wp-config.txt里找到数据库账号密码
![assets/Brute4Road打靶flag1-2（待完结/file-20260325195328336.png](/assets/cnblogs/Brute4Road打靶flag1-2（待完结/3539156-20260325204904443-428189572.png)
找到flag2表
![assets/Brute4Road打靶flag1-2（待完结/file-20260325195413293.png](/assets/cnblogs/Brute4Road打靶flag1-2（待完结/3539156-20260325204904465-487615931.png)
## flag3
随后发现上面很奇怪，打开看是个密码表
![assets/Brute4Road打靶flag1-2（待完结/file-20260325195555044.png](/assets/cnblogs/Brute4Road打靶flag1-2（待完结/3539156-20260325204904503-831126810.png)
导出成csv后尝试爆破
再看前面，估计只有172.22.2.16的密码是需要爆破的（mssql）
./fscan -h 172.22.2.16 -m mssql  -pwdf 1.txt -user sa
[+] mssql:172.22.2.16:1433:sa ElGNkOiC

后面的先挖个坑，电脑proxifier装不好了（哭
