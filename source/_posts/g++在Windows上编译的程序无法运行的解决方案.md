---
title: "g++在Windows上编译的程序无法运行的解决方案"
date: 2025-06-27 20:11:00
categories:
  - "Programming"
tags:
  - "Programming"
  - "C++"
cnblogs_postid: "18952940"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18952940"
---

最近想用cpeditor做题，发现怎么都是报错
![image](/assets/cnblogs/g++在Windows上编译的程序无法运行的解决方案/3539156-20250627200849105-386803151.png)
尝试多次无果，最后单独运行g++编译的程序才发现编译的程序有问题
![image](/assets/cnblogs/g++在Windows上编译的程序无法运行的解决方案/3539156-20250627200919975-1518892041.png)
问题： MinGW-W64 使用的是 ​UCRT​（Universal C Runtime），而某些旧代码或依赖可能默认链接到 ​MSVCRT​（传统运行时库），导致运行时冲突
解决方案：
加上`-D__USE_MINGW_ANSI_STDIO=1 -static `即可，这样就可以运行了
![image](/assets/cnblogs/g++在Windows上编译的程序无法运行的解决方案/3539156-20250627201042251-1494662066.png)
（完整的：`g++ -Wall -std=c++14 -O2 -D__USE_MINGW_ANSI_STDIO=1 -static `）
