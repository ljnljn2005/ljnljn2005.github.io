---
title: "gdb调试小技巧——多个窗口显示"
date: 2025-01-23 12:14:00
categories:
  - "CTF Writeup"
tags:
  - "CTF"
  - "Writeup"
  - "Pwn"
cnblogs_postid: "18687523"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18687523"
---

先用tty显示需要显示的终端的序号
```
┌──(root㉿kali)-[~]
└─# tty
/dev/pts/3
```
然后
```
vim ~/.gdbinit
```
在文件后加一行
```
set context-output /dev/pts/2
```
这里数字就是tty显示的数字
设置好之后打开gdb时就可以了
![image](/assets/cnblogs/gdb调试小技巧——多个窗口显示/3539156-20250123121314971-1816362094.png)
