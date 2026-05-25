---
title: "volatility2指令"
date: 2024-11-23 23:02:00
categories:
  - "CTF Misc"
tags:
  - "CTF"
  - "Misc"
cnblogs_postid: "18565237"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18565237"
---

1、检查该内存镜像操作系统（服务号/32/64）、获取时间
```volatility -f mem.vmem imageinfo ```
2、列出该内存的所有进程信息
```volatility -f mem.vmem --profile=xx pslist    ```
      提取出进程的文件
  ```volatility -f mem.vmem --profile=xx procdump -p 1736 -D E:/```
3、是否有隐藏进程信息
```volatility -f name --profile=xx psscan ```
4、缓存在内存的注册表
```volatility -f mem.vmem --profile=xx hivelist```
5、打印注册表中的数据
```volatility -f mem.vmem --profile=xx hivedump -o 0xe16aab60```
6、获取SAM表中的用户
```volatility -f mem.vmem --profile=xx printkey -K "SAM\Domains\Account\Users\Names"```
7、获取最后登录系统的用户
```volatility -f mem.vmem –profile=xx printkey -K "SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"```
8、提取出内存中记录的 当时正在运行的程序有哪些，运行过多少次，最后一次运行的时间等信息
```volatility -f mem.vmem --profile=xx userassist```
9、将内存中的某个进程数据以 dmp 的格式保存出来
```mkdir ctfmon
volatility -f mem.vmem --profile=xx memdump -p 1736 -D ctfmon/
```
后续可以使用16进制编辑器分析，或使用strings提取其中的字符串分析
10、提取内存中保留的 cmd 命令使用情况
```volatility -f mem.vmem --profile=xx cmdscan```
11、查看网络连接情况
```volatility -f mem.vmem --profile=xx netscan```
12、获取 IE 浏览器的使用情况
```volatility -f mem.vmem --profile=xx iehistory```
13、获取动态链接库
```volatility -f name --profile=WinXPSP2x8 dlllist 动态链接库文件 （Dynamic Link Library）```
14、获取内存中的系统密码（获取用户登入密码的 NTLM hash）
```volatility -f easy_dump.img --profile=Win7SP1x64 hashdump 
volatility -f mem.vmem --profile=xx hivelist
volatility -f mem.vmem --profile=xx hashdump -y 0xe1035b60 -s 0xe16aab60```
15、最大程度上将内存中的信息提取出来，那么你可以使用 timeliner 这个插件。它会从多个位置来收集系统的活动信息
```volatility -f mem.vmem –profile=xx timeliner```
16、查找镜像中的文件
```volatility -f forensics.raw --profile=Win7SP1x64 filescan | grep/findstr “zip|txt|jpg|png”
```
17、获取剪切板中的数据
```volatility -f name --profile=Win7SP1x64 clipboard```
18、内存中的缓存文件
```volatility -f name --profile=Win7SP1x64 filescan (刷屏)
volatility -f flag --profile=xx filescan | grep rar  文件过滤
```
19、获取用户的SID
```volatility -f mem.vmem --profile=xx getsids```
20、获取某文件什么时间被访问过，以及路径
```volatility -f mem.vmem --profile=xx mftparser```
21、获取主机名 注册表键值 printkey hostname计算机名称
 ```volatility -f 1.vmem --profile=Win7SP1x64 printkey -K "ControlSet001\Control\ComputerName\ComputerName"```
22、列出username系统用户名 printkey
 ```volatility -f 1.vmem --profile=Win7SP1x64 printkey -K "SAM\Domains\Account\Users\Names"```
23、如果hashdump出来的结果 john跑不出来 用lsadump来解决 得到强密码
 ```volatility -f 1.vmem --profile=Win7SP1x64 lsadump```
24.导出内存镜像中的文件
 ```volatility -f mem.vmem --profile=Win7SP1x64 dumpfiles -Q 0x000000007f2b88b0 -D ./ -u```
25.查看记事本内容
 ```.\volatility.exe -f .\mem.raw --profile=Win7SP1x64 editbox```
