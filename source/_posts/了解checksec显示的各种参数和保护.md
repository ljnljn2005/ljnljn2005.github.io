---
title: "了解checksec显示的各种参数和保护"
date: 2024-12-04 21:06:00
categories:
  - "CTF Writeup"
tags:
  - "CTF"
  - "Writeup"
  - "Pwn"
cnblogs_postid: "18587196"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18587196"
---

![image](/assets/cnblogs/了解checksec显示的各种参数和保护/3539156-20241204203254343-1540893652.png)
## Arch：内核（32位/64位）
## RELRO
在Linux系统安全领域数据可以写的存储区就会是攻击的目标，尤其是存储函数指针的区域。所以在安全防护的角度来说尽量减少可写的存储区域对安全会有极大的好处.
GCC, GNU linker以及Glibc-dynamic linker一起配合实现了一种叫做relro的技术: read only relocation。大概实现就是由linker指定binary的一块经过dynamic linker处理过 relocation之后的区域为只读.
RELRO重定位段只读保护分为以下三个等级：
- NO RELRO：保护未开的情况，所有重定位段均可写，包括.dynamic、.got、.got.plt；
- Partial RELRO：部分开启保护，其为GCC编译的默认配置。.dynamic、.got被标记为只读，并且会强制地将ELF的内部数据段 .got ，.got.plt等放到外部数据段 .data、.bss之前，即防止程序数据段溢出改变内部数据段的值，从而劫持程序控制流。虽然.got标记为只读，但是.got.plt仍然可写，即仍然可以改写GOT表劫持程序控制流；
- Full RELRO：继承Partial RELRO的所有保护，并且.got.plt也被标为只读。此时延迟绑定技术被禁止，所有的外部函数地址将在程序装载时解析、装入，并标记为只读，不可更改。此时不需要link_map以及dl_runtime_resolve函数，则GOT表中这两项数据均置为0，此时ret2dlresolve技术最关键的两项数据丢失，并且GOT表不可写。

介绍RELRO与Pwn：https://bbs.kanxue.com/thread-282512.htm

## Stack(栈检查)
canary（栈保护）
栈溢出保护是一种缓冲区溢出攻击缓解手段，当函数存在缓冲区溢出攻击漏洞时，攻击者可以覆盖栈上的返回地址来让shellcode能够得到执行。当启用栈保护后，函数开始执行的时候会先往栈里插入cookie信息，当函数真正返回的时候会验证cookie信息是否合法，如果不合法就停止程序运行。攻击者在覆盖返回地址的时候往往也会将cookie信息给覆盖掉，导致栈保护检查失败而阻止shellcode的执行。在Linux中我们将cookie信息称为canary。

## NX
NX即No-eXecute（不可执行）的意思，NX（DEP）的基本原理是将数据所在内存页标识为不可执行，当程序溢出成功转入shellcode时，程序会尝试在数据页面上执行指令，此时CPU就会抛出异常，而不是去执行恶意指令。

## PIE
一般情况下NX（Windows平台上称其为DEP）和地址空间分布随机化（ASLR）会同时工作。内存地址随机化机制（address space layout randomization)，有以下三种情况
0 - 表示关闭进程地址空间随机化。
1 - 表示将mmap的基址，stack和vdso页面随机化。
2 - 表示在1的基础上增加堆（heap）的随机化。
可以防范基于Ret2libc方式的针对DEP的攻击。ASLR和DEP配合使用，能有效阻止攻击者在堆栈上运行恶意代码。
Built as PIE：位置独立的可执行区域（position-independent executables）。这样使得在利用缓冲溢出和移动操作系统中存在的其他内存崩溃缺陷时采用面向返回的编程（return-oriented programming）方法变得难得多。
## Stripped
stripped：将程序中的符号表的信息剔除掉了，这样子编译出来的可执行文件体积比较小；
not stripped：则反之，但是就是因为其保留了这些信息，所以便于调试。

参考资料：
https://blog.csdn.net/panfengsoftware/article/details/7775108
https://blog.csdn.net/qq_44108455/article/details/104985351
https://www.testzero-wz.com/2022/03/05/Ret2dlresolve%E2%80%94%E2%80%94%E4%BB%8ENo-RELRO%E5%88%B0FULL-RELRO/
