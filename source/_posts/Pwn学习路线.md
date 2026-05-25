---
title: "Pwn学习路线"
date: 2024-11-30 17:38:00
categories:
  - "CTF Writeup"
tags:
  - "CTF"
  - "Writeup"
  - "Pwn"
cnblogs_postid: "18578683"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18578683"
---

> 来源：CTF竞赛权威指南（Pwn篇）
## 1、底层代码学习
编程基础：Python/C/C++/汇编语言
其他知识：计算机组成原理、操作系统、编译原理
课程：
网易云课堂的“顶尖中文大学计算机专业课程体系”
https://study.163.com/curricula/cs.htm
![image](/assets/cnblogs/Pwn学习路线/3539156-20241130172520418-138847279.png)
## 2、静态反编译
熟练掌握IDA、Radre2等
熟练阅读反汇编代码，理解x86、ARM、MIPS二进制程序
## 3、动态调试
熟练掌握GDB、x64dbg等
2/3推荐资料：
- Secure Coding in C and C++, 2nd Edition(TP312C/775)
- The Intel 64 and IA-32 Architectures Software Developer's Manual
- ARM Cortex - A Series Programmer's Guide
- See MIPS Run, 2nd Edition
- Reverse Engineering for Beginners
- 《程序员的自我修养 —— 链接、装载与库》（TP311.1/65）
- 《加密与解密，第 4 版》
## 4.软件漏洞学习
多读WriteUp
- 常见漏洞（溢出、UAF、double - free 等）的原理
- Linux 漏洞缓解机制（Stack canaries、NX、ASLR 等）
- 针对这些机制的漏洞利用方法（Stack Smashing、Shellcoding、ROP 等）
推荐资料：
- RPI CSCI - 4968 Modern Binary Exploitation
- Hacking: The Art of Exploitation, 2nd Edition
- The Shellcoder's Handbook, 2nd Edition
- Practical Malware Analysis
- 《漏洞战争：软件漏洞分析精要》
## 5.程序分析理论
- 数据流分析（工具如 Soot）
- 值集分析（BAP）
- 可满足性理论（Z3）
- 动态二进制插桩（DynamoRio、Pin）
- 符号执行（KLEE、angr）
- 模糊测试（Peach、AFL）
这些技术对于将程序分析和漏洞挖掘自动化非常重要，是学术界和工业界都在研究的热点。
感兴趣的还可以关注一下专注于自动化网络攻防的 CGC 竞赛。
推荐资料：
- UT Dallas CS-6V81 System Security and Binary Code Analysis
- AU Static Program Analysis Lecture notes
## 6.继续提升
- 阅读论文
- 收集和订阅一些安全资讯（FreeBuf、SecWiki、安全客）、漏洞披露（exploit - db、CVE）、技术论坛（看雪论坛、吾爱破解、先知社区）和大牛的技术博客，这一步可以通过 RSS Feed（我用的tiny tiny rss）来完成。
- 随着社会媒体的发展，很多安全团队和个人都转战到了 Twitter、微博、微信公众号等新媒体上，请果断关注他们（操作技巧：从某个安全研究者开始，遍历其关注列表，然后递归）
