---
title: "2024第一届Solar杯应急响应挑战赛WP"
date: 2024-12-28 19:54:00
categories:
  - "Forensics Writeup"
tags:
  - "Forensics"
  - "Writeup"
  - "Solar杯"
cnblogs_postid: "18637872"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18637872"
---

对于一个只学了2个月的小白来说这种比赛难度还是太高了，还要沉淀一下QAQ
> 附件链接：https://pan.baidu.com/s/1MPFLliLcLeJCdhYLSp8oVw?pwd=ky34
所有附件解压密码均为：KzXGabLkDjs&j@3a&fAayNmD
## 1、内存取证-1
题目描述
题目文件：SERVER-2008-20241220-162057
请找到rdp连接的跳板地址
flag格式 flag\{1.1.1.1\}
先imageinfo
![image](/assets/cnblogs/2024第一届Solar杯应急响应挑战赛WP/3539156-20241228185928869-520489624.png)
然后netscan
```
F:\CTF软件合集\Misc杂项\隐写工具\取证类\volatility\VolatilityWorkbench-内存取证\volatility2>volatility.exe -f F:\应急比 赛\SERVER-2008-20241220-162057.raw --profile=Win2008R2SP0x64 netscan
Volatility Foundation Volatility Framework 2.6
Offset(P)          Proto    Local Address                  Foreign Address      State            Pid      Owner          Created
0x7db8b220         UDPv6    fe80::ecdb:a57f:7f20:cff4:546  *:*                                   728      svchost.exe    2024-12-20 16:19:54 UTC+0000
0x7e387010         UDPv4    192.168.60.150:138             *:*                                   4        System         2024-12-20 16:12:38 UTC+0000
0x7e3cd820         UDPv4    0.0.0.0:41163                  *:*                                   2068     firefox.exe    2024-12-20 16:18:36 UTC+0000
0x7e3cf830         UDPv4    0.0.0.0:5355                   *:*                                   972      svchost.exe    2024-12-20 16:12:39 UTC+0000
0x7e3cf830         UDPv6    :::5355                        *:*                                   972      svchost.exe    2024-12-20 16:12:39 UTC+0000
0x7e2536a0         TCPv4    0.0.0.0:49155                  0.0.0.0:0            LISTENING        472      services.exe

0x7e2536a0         TCPv6    :::49155                       :::0                 LISTENING        472      services.exe

0x7e2598b0         TCPv4    0.0.0.0:49155                  0.0.0.0:0            LISTENING        472      services.exe

0x7e2bf580         TCPv4    192.168.60.150:139             0.0.0.0:0            LISTENING        4        System

0x7e300dc0         TCPv4    0.0.0.0:3389                   0.0.0.0:0            LISTENING        1908     svchost.exe

0x7e303360         TCPv4    0.0.0.0:3389                   0.0.0.0:0            LISTENING        1908     svchost.exe

0x7e303360         TCPv6    :::3389                        :::0                 LISTENING        1908     svchost.exe

0x7de11010         TCPv4    -:49196                        -:443                CLOSED           2068     firefox.exe

0x7de65cf0         TCPv4    -:49263                        155.94.204.67:85     CLOSED           504

0x7de89540         TCPv4    192.168.60.150:445             192.168.60.169:46087 CLOSED           4        System

0x7dec4480         TCPv4    192.168.60.150:49261           34.117.188.166:443   ESTABLISHED      2068     firefox.exe

0x7decc010         TCPv4    192.168.60.150:3389            192.168.60.220:34121 ESTABLISHED      1908     svchost.exe

0x7ded2ba0         TCPv4    192.168.60.150:49185           34.107.243.93:443    ESTABLISHED      2068     firefox.exe

0x7dee98d0         TCPv6    -:0                            e81a:da18:80fa:ffff:e81a:da18:80fa:ffff:0 CLOSED           2068     firefox.exe
0x7df56cf0         TCPv4    192.168.60.150:49257           192.168.60.169:4444  ESTABLISHED      828      spoolsv.exe

0x7e008cf0         TCPv4    127.0.0.1:49161                127.0.0.1:49160      ESTABLISHED      2472     firefox.exe

0x7e009010         TCPv4    127.0.0.1:49160                127.0.0.1:49161      ESTABLISHED      2472     firefox.exe

0x7e1ecb30         TCPv4    -:49194                        -:443                CLOSED           2068     firefox.exe

0x7e2d9150         TCPv4    127.0.0.1:49159                127.0.0.1:49158      ESTABLISHED      2068     firefox.exe

0x7e7bae40         UDPv4    192.168.60.150:137             *:*                                   4        System         2024-12-20 16:12:38 UTC+0000
0x7e5ff650         TCPv4    0.0.0.0:80                     0.0.0.0:0            LISTENING        4        System

0x7e5ff650         TCPv6    :::80                          :::0                 LISTENING        4        System

0x7e644840         TCPv4    0.0.0.0:445                    0.0.0.0:0            LISTENING        4        System

0x7e644840         TCPv6    :::445                         :::0                 LISTENING        4        System

0x7e673ef0         TCPv4    0.0.0.0:49154                  0.0.0.0:0            LISTENING        808      svchost.exe

0x7e673ef0         TCPv6    :::49154                       :::0                 LISTENING        808      svchost.exe

0x7e6ed010         TCPv4    0.0.0.0:135                    0.0.0.0:0            LISTENING        656      svchost.exe

0x7e6ed010         TCPv6    :::135                         :::0                 LISTENING        656      svchost.exe

0x7e6efce0         TCPv4    0.0.0.0:135                    0.0.0.0:0            LISTENING        656      svchost.exe

0x7e6f58c0         TCPv4    0.0.0.0:49152                  0.0.0.0:0            LISTENING        368      wininit.exe

0x7e6fac90         TCPv4    0.0.0.0:49152                  0.0.0.0:0            LISTENING        368      wininit.exe

0x7e6fac90         TCPv6    :::49152                       :::0                 LISTENING        368      wininit.exe

0x7e735180         TCPv4    0.0.0.0:49153                  0.0.0.0:0            LISTENING        728      svchost.exe

0x7e735180         TCPv6    :::49153                       :::0                 LISTENING        728      svchost.exe

0x7e7369d0         TCPv4    0.0.0.0:49153                  0.0.0.0:0            LISTENING        728      svchost.exe

0x7e78f010         TCPv4    0.0.0.0:49154                  0.0.0.0:0            LISTENING        808      svchost.exe

0x7e6ef400         TCPv4    -:0                            168.148.77.26:0      CLOSED           48       N

0x7e6f2cf0         TCPv6    -:0                            a894:4d1a:80fa:ffff:a894:4d1a:80fa:ffff:0 CLOSED           1        ??3????
0x7e735cf0         TCPv6    -:0                            385b:501a:80fa:ffff:385b:501a:80fa:ffff:0 CLOSED           1        ??3????
0x7ee2f6c0         UDPv4    0.0.0.0:0                      *:*                                   972      svchost.exe    2024-12-20 16:12:38 UTC+0000
0x7ee2f6c0         UDPv6    :::0                           *:*                                   972      svchost.exe    2024-12-20 16:12:38 UTC+0000
0x7ee3e4b0         UDPv4    0.0.0.0:5355                   *:*                                   972      svchost.exe    2024-12-20 16:12:39 UTC+0000
0x7ee1cdb0         TCPv4    0.0.0.0:49156                  0.0.0.0:0            LISTENING        480      lsass.exe

0x7ee1cdb0         TCPv6    :::49156                       :::0                 LISTENING        480      lsass.exe

0x7ee1ebc0         TCPv4    0.0.0.0:49156                  0.0.0.0:0            LISTENING        480      lsass.exe

0x7f0fbcf0         TCPv4    127.0.0.1:49158                127.0.0.1:49159      ESTABLISHED      2068     firefox.exe

0x7fc3fef0         TCPv4    0.0.0.0:47001                  0.0.0.0:0            LISTENING        4        System

0x7fc3fef0         TCPv6    :::47001                       :::0                 LISTENING        4        System
```
这里为了省事直接问ai了（绝对不是我不会
> 从给出的信息中查找 RDP（Remote Desktop Protocol，远程桌面协议，默认使用 TCP 3389 端口）连接相关的内容来确定跳板地址，以下是分析过程：
> 1. 筛选出 RDP 相关连接记录
在这些网络连接信息中，关注目标端口为 3389 的 TCP 连接记录，相关记录如下：
plaintext
0x7e300dc0         TCPv4    0.0.0.0:3389                   0.0.0.0:0            LISTENING        1908     svchost.exe
0x7e303360         TCPv4    0.0.0.0:3389                   0.0.0.0:0            LISTENING        1908     svchost.exe
0x7e303360         TCPv6    :::3389                        :::0                 LISTENING        1908     svchost.exe
0x7decc010         TCPv4    192.168.60.150:3389            192.168.60.220:34121 ESTABLISHED      1908     svchost.exe
> 2. 确定跳板地址
在上述记录中，对于已经建立（ESTABLISHED）的 RDP 连接 0x7decc010 TCPv4 192.168.60.150:3389 192.168.60.220:34121 ESTABLISHED 1908 svchost.exe ，本地地址为 192.168.60.150 ，而与之建立连接的远程地址（也就是可能的跳板地址或者连接的对端地址）是 192.168.60.220 。
所以，从当前提供的信息来看，此 RDP 连接对应的跳板地址（或连接对端地址）为 192.168.60.220 。

ip地址即为flag
## 2、内存取证-2
还是上面的命令，中间找到一个没有owner的ip很可疑，一搜发现是美国的，因此可以认定为答案
![image](/assets/cnblogs/2024第一届Solar杯应急响应挑战赛WP/3539156-20241228193354005-554022902.png)

## 3、内存取证-3
题目描述
题目文件：SERVER-2008-20241220-162057
攻击者获取的“FusionManager节点操作系统帐户（业务帐户）”的密码是什么
flag格式 flag{xxxx}

先查txt
![image](/assets/cnblogs/2024第一届Solar杯应急响应挑战赛WP/3539156-20241228190302626-339632246.png)
发现pass.txt很可疑，于是导出
![image](/assets/cnblogs/2024第一届Solar杯应急响应挑战赛WP/3539156-20241228190338320-1171084344.png)
在txt里搜业务账户和fusion找出密码
![image](/assets/cnblogs/2024第一届Solar杯应急响应挑战赛WP/3539156-20241228190446056-302044287.png)

## 4、内存取证-4
题目描述
题目文件：SERVER-2008-20241220-162057
请找到攻击者创建的用户
flag格式 flag{xxxx}

这里试了一下是ASP.NET
![image](/assets/cnblogs/2024第一届Solar杯应急响应挑战赛WP/3539156-20241228190532552-1326051789.png)

## 5、内存取证-5
题目描述
题目文件：SERVER-2008-20241220-162057
请找到攻击者利用跳板rdp登录的时间
flag格式 flag{2024/01/01 00:00:00}

用工具找的
![image](/assets/cnblogs/2024第一届Solar杯应急响应挑战赛WP/3539156-20241228193736689-263992702.png)


## 6、内存取证-6
题目描述
题目文件：SERVER-2008-20241220-162057
请找到攻击者创建的用户的密码哈希值
flag格式 flag{XXXX}

还是用工具找的（不知道为什么volatility输进去哈希值不对）
![image](/assets/cnblogs/2024第一届Solar杯应急响应挑战赛WP/3539156-20241228190807316-1307826030.png)

## 7、签到
题目描述
本题作为签到题,请给出邮服发件顺序。

Received: from mail.da4s8gag.com ([140.143.207.229])
by newxmmxszc6-1.qq.com (NewMX) with SMTP id 6010A8AD
for ; Thu, 17 Oct 2024 11:24:01 +0800
X-QQ-mid: xmmxszc6-1t1729135441tm9qrjq3k
X-QQ-XMRINFO: NgToQqU5s31XQ+vYT/V7+uk=
Authentication-Results: mx.qq.com; spf=none smtp.mailfrom=;
dkim=none; dmarc=none(permerror) header.from=solar.sec
Received: from mail.solar.sec (VM-20-3-centos [127.0.0.1])
by mail.da4s8gag.com (Postfix) with ESMTP id 2EF0A60264
for ; Thu, 17 Oct 2024 11:24:01 +0800 (CST)
Date: Thu, 17 Oct 2024 11:24:01 +0800
To: hellosolartest@qq.com
From: 鍏嬪競缃戜俊
Subject:xxxxxxxxxx
Message-Id: <20241017112401.032146@mail.solar.sec>
X-Mailer: QQMail 2.x

XXXXXXXXXX

flag格式为flag{domain1|...|domainN}

没啥说的
flag{mail.solar.sec|mail.da4s8gag.com|newxmmxszc6-1.qq.com}

## 8、数据库-1
题目描述
题目附件：mssql、mssql题-备份数据库
请找到攻击者创建隐藏账户的时间
flag格式 如 flag{2024/01/01 00:00:00}

下面时间和上面20个账户都不同，所以输下面的
![image](/assets/cnblogs/2024第一届Solar杯应急响应挑战赛WP/3539156-20241228191034992-1129121944.png)

以下是复盘结果：
## 9、日志流量-1
题目描述
题目文件：tomcat-wireshark.zip/web
新手运维小王的Geoserver遭到了攻击：
黑客疑似删除了webshell后门，小王找到了可能是攻击痕迹的文件但不一定是正确的，请帮他排查一下。
flag格式 flag{xxxx}

比赛的时候一直尝试破class，但是因为环境没配好所以一直失败
这里的方法：
1、用D盾扫webshell后门
![image](/assets/cnblogs/2024第一届Solar杯应急响应挑战赛WP/3539156-20241228191455313-1866068935.png)
找到java文件后直接打开，发现base64加密
![image](/assets/cnblogs/2024第一届Solar杯应急响应挑战赛WP/3539156-20241228191519729-268218049.png)
解密后获得flag
![image](/assets/cnblogs/2024第一届Solar杯应急响应挑战赛WP/3539156-20241228191535425-917370440.png)

## 10、数据库-2
题目描述
题目附件：mssql、mssql题-备份数据库
请找到恶意文件的名称
flag格式 如 flag{*.*}

这里比赛的时候不知道怎么回事用火绒怎么都扫不出来病毒，估计是自动查杀掉了

先用火眼找一下密码
![image](/assets/cnblogs/2024第一届Solar杯应急响应挑战赛WP/3539156-20241228194530495-1305320454.png)

然后找病毒（这里火绒扫到了installer和uninstaller就是没扫到xmrig，无大语）
![image](/assets/cnblogs/2024第一届Solar杯应急响应挑战赛WP/3539156-20241228194622689-154114338.png)
扔云沙箱里果然是木马
![image](/assets/cnblogs/2024第一届Solar杯应急响应挑战赛WP/3539156-20241228194906111-1451132141.png)

## 11、数据库-3
题目描述
题目附件：mssql、mssql题-备份数据库
请找到恶意文件的外联地址
flag格式 如 flag{1.1.1.1}

用CurrPorts找到软件外联ip
![image](/assets/cnblogs/2024第一届Solar杯应急响应挑战赛WP/3539156-20241228195256317-1991680418.png)

## 12、数据库-4
修复数据库
Solar官方对病毒进行的分析：
https://blog.csdn.net/solarset/article/details/144318706
其中有两句：
![image](/assets/cnblogs/2024第一届Solar杯应急响应挑战赛WP/3539156-20241229082425045-1030787760.png)

![image](/assets/cnblogs/2024第一届Solar杯应急响应挑战赛WP/3539156-20241229082409823-1749059361.png)
猜测flag根本就没出问题，直接找到数据库路径后开搜

![image](/assets/cnblogs/2024第一届Solar杯应急响应挑战赛WP/3539156-20241229082623020-77774159.png)
