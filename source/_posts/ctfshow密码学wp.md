---
title: "ctfshow密码学wp"
date: 2025-02-06 23:02:00
categories:
  - "CTF Writeup"
tags:
  - "CTF"
  - "Writeup"
  - "ctfshow"
  - "Web"
  - "Crypto"
cnblogs_postid: "18701839"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18701839"
---

打hgame打傻了来洗洗脑子（
## 1、密码学签到
![image](/assets/cnblogs/ctfshow密码学wp/3539156-20250206223504478-838601657.png)
## 2、
jsfuck扔控制台
![image](/assets/cnblogs/ctfshow密码学wp/3539156-20250206223621487-933630638.png)
## 3、
aaencode颜文字
![image](/assets/cnblogs/ctfshow密码学wp/3539156-20250206224115182-1571246666.png)
## 4、
ctfrsatools
![image](/assets/cnblogs/ctfshow密码学wp/3539156-20250206224532635-1528416048.png)
```
from Crypto.Util.number import *  
from gmpy2 import *  
p=447685307  
q=2037  
e=17  
phi=(p-1)*(q-1)  
d=inverse(e,phi)  
print(d)  
```
## 5、
交int
![image](/assets/cnblogs/ctfshow密码学wp/3539156-20250206224634355-507569953.png)
```
import gmpy2,libnum  
from Crypto.Util.number import long_to_bytes  
c = 704796792  
p = 447685307  
q = 2037  
e = 17  
d = gmpy2.invert(e, (p-1)*(q-1))  
m = pow(c, d, p*q)  
print(m)  
```
## 6、
U2FsdGVkX1开头，猜测是rabbit加密。
![image](/assets/cnblogs/ctfshow密码学wp/3539156-20250206225045885-2018840326.png)
## 7、
ook
https://www.splitbrain.org/services/ook
![image](/assets/cnblogs/ctfshow密码学wp/3539156-20250206225311897-916935890.png)
##  8、
brainfuck
![image](/assets/cnblogs/ctfshow密码学wp/3539156-20250206225405636-1603956412.png)
## 9、
先爆破
![image](/assets/cnblogs/ctfshow密码学wp/3539156-20250206225554094-306775269.png)
文件找不到方向，再看压缩包名字serpent，搜索发现是加密形式
![image](/assets/cnblogs/ctfshow密码学wp/3539156-20250206230132129-566853827.png)
