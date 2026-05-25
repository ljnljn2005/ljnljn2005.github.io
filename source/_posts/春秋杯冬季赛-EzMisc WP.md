---
title: "春秋杯冬季赛-EzMisc WP"
date: 2025-01-19 19:00:00
categories:
  - "CTF Writeup"
tags:
  - "CTF"
  - "Writeup"
  - "春秋杯"
  - "Misc"
cnblogs_postid: "18679811"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18679811"
---

后面两天本来没打算写出来啥题的，因为都太难了呜呜，但是这道题竟然做出来了（虽然花了接近3个小时），还是有点小激动

## 前排提醒

1、是看了提示之后才做出来的

> 题目提示：1、利⽤DP泄露来求出私钥，从⽽还原私钥流解密密⽂ 2、图片经过了Arnold变换

2、存在偶然性，复现难度挺大的，大佬轻点喷QAQ

## 解答过程

### 1、流量分析

直接追踪流走起

![image](/assets/cnblogs/春秋杯冬季赛-EzMisc WP/3539156-20250119184715193-1355920193.png)


这时候显示设置为UTF-8

第五个流显示有三个文件，私钥、压缩包、密文

```
-rw-------    1 ftp      ftp           256 Oct 24 12:06 encrypted.enc
-rw-------    1 ftp      ftp         31168 Oct 24 12:06 flag.7z
-rw-------    1 ftp      ftp          1679 Oct 24 12:04 private_key.pem
```

在第六个流显示传输私钥

```
150 Opening BINARY mode data connection for private_key.pem (1679 bytes).
226 Transfer complete.
```

第七个流就是私钥

说明格式都是文件名-文件内容

因此导出第7个流（另存为）为private_key.pem，第10个流为encrypted.enc

注意这里第10个流和12个流是二进制文件，要用“显示为原始数据”存储

这样我们就得到了三个文件

### 2、修复私钥

用openssl看私钥是否正确，结果是错的（不然怎么会卡到这里

![image](/assets/cnblogs/春秋杯冬季赛-EzMisc WP/3539156-20250119184655534-479946638.png)


现在就用到了提示1：利⽤DP泄露来求出私钥，从⽽还原私钥流解密密⽂

先对这个坏的私钥进行分析（这里只需要n和dp，就只拿出这两个）

```
E:\>openssl rsa -in PRIVATEKEY.pem -text
Private-Key: (2048 bit, 2 primes)
modulus:
    00:b3:ee:84:a7:c4:9a:b1:b8:6f:20:6e:b6:89:18:
    00:aa:9a:42:ec:4e:b1:b4:cd:de:74:f7:67:eb:9e:
    07:d0:82:09:72:bd:d3:b2:2b:3c:38:ee:49:70:49:
    52:1e:12:64:0a:44:f5:c6:d4:60:1e:6d:73:57:23:
    c8:a7:36:53:3d:96:37:bc:c8:0d:fb:14:ee:0f:09:
    fb:ae:83:eb:30:9f:68:62:15:04:f1:8b:77:94:11:
    a8:b4:ec:99:87:bf:df:4a:af:e1:77:d2:00:4e:a9:
    8e:de:04:e0:07:34:05:14:f2:8a:f8:d2:c7:86:27:
    58:60:49:1b:83:b3:23:d9:30:9a:48:e6:4e:66:d9:
    1a:ec:bb:0f:7e:39:eb:d9:ba:3f:87:73:2f:24:0c:
    7c:e9:11:03:3b:61:57:bc:90:21:63:d0:3f:56:20:
    5a:b6:ad:29:18:a0:ff:2e:2a:07:93:06:9f:8d:dd:
    ab:c5:00:37:4a:39:ee:af:c2:f1:39:67:8c:f6:73:
    59:91:94:78:0c:7f:e4:93:11:cb:2b:1b:25:45:e3:
    c6:90:e1:db:2e:0c:08:3b:d6:dd:a6:58:48:d6:4c:
    bb:81:0a:42:43:79:a8:8b:be:15:3d:df:3c:8e:79:
    e0:c8:07:ed:1a:a9:b6:87:43:30:da:35:59:83:0c:
    fa:45
publicExponent: 65537 (0x10001)
privateExponent:...
prime1:...
prime2:...
exponent1:
    00:97:24:1a:2c:d4:a3:a6:a6:24:57:ed:7a:08:bd:
    ae:42:85:aa:8a:a5:c8:2f:74:13:a0:d8:64:32:97:
    cb:44:ad:e7:e6:25:d2:9c:de:1a:6a:2d:9d:0c:2a:
    b6:7e:1a:81:64:70:ad:47:08:b7:92:f9:73:38:7c:
    fb:90:5e:47:3d:bb:2e:4b:70:da:2a:4e:74:62:f4:
    53:1b:c1:cb:a0:bc:fb:04:b6:0e:49:b5:eb:05:c3:
    4d:8e:91:48:ac:12:e9:a9:ce:34:d7:c7:af:73:e9:
    c6:be:76:94:2d:e1:f0:35:73:4f:6b:58:65:08:d1:
    57:80:9e:3e:9d:ed:df:fc:a7
exponent2:...
coefficient:...
```

修改一下格式（去掉冒号和空格，前面加0x）

n=0x00b3ee84a7c49ab1b86f206eb6891800aa9a42ec4eb1b4cdde74f767eb9e07d0820972bdd3b22b3c38ee497049521e12640a44f5c6d4601e6d735723c8a736533d9637bcc80dfb14ee0f09fbae83eb309f68621504f18b779411a8b4ec9987bfdf4aafe177d2004ea98ede04e007340514f28af8d2c786275860491b83b323d9309a48e64e66d91aecbb0f7e39ebd9ba3f87732f240c7ce911033b6157bc902163d03f56205ab6ad2918a0ff2e2a0793069f8dddabc500374a39eeafc2f139678cf673599194780c7fe49311cb2b1b2545e3c690e1db2e0c083bd6dda65848d64cbb810a424379a88bbe153ddf3c8e79e0c807ed1aa9b6874330da3559830cfa45

dp=0x0097241a2cd4a3a6a62457ed7a08bdae4285aa8aa5c82f7413a0d8643297cb44ade7e625d29cde1a6a2d9d0c2ab67e1a816470ad4708b792f973387cfb905e473dbb2e4b70da2a4e7462f4531bc1cba0bcfb04b60e49b5eb05c34d8e9148ac12e9a9ce34d7c7af73e9c6be76942de1f035734f6b586508d157809e3e9deddffca7

然后求解p、q，到网上搜了个代码，因为没有密文所以修改了一下

[RSA的dp泄露 [BUUCTF\] RSA2_dp=d%(p-1)-CSDN博客](https://blog.csdn.net/weixin_45859850/article/details/109559190)

```
import gmpy2 as gp
e = 65537
n=0x00b3ee84a7c49ab1b86f206eb6891800aa9a42ec4eb1b4cdde74f767eb9e07d0820972bdd3b22b3c38ee497049521e12640a44f5c6d4601e6d735723c8a736533d9637bcc80dfb14ee0f09fbae83eb309f68621504f18b779411a8b4ec9987bfdf4aafe177d2004ea98ede04e007340514f28af8d2c786275860491b83b323d9309a48e64e66d91aecbb0f7e39ebd9ba3f87732f240c7ce911033b6157bc902163d03f56205ab6ad2918a0ff2e2a0793069f8dddabc500374a39eeafc2f139678cf673599194780c7fe49311cb2b1b2545e3c690e1db2e0c083bd6dda65848d64cbb810a424379a88bbe153ddf3c8e79e0c807ed1aa9b6874330da3559830cfa45
dp=0x0097241a2cd4a3a6a62457ed7a08bdae4285aa8aa5c82f7413a0d8643297cb44ade7e625d29cde1a6a2d9d0c2ab67e1a816470ad4708b792f973387cfb905e473dbb2e4b70da2a4e7462f4531bc1cba0bcfb04b60e49b5eb05c34d8e9148ac12e9a9ce34d7c7af73e9c6be76942de1f035734f6b586508d157809e3e9deddffca7
for i in range(1, e):
    if (dp * e - 1) % i == 0:
        if n % (((dp * e - 1) // i) + 1) == 0:
            p = ((dp * e - 1) // i) + 1
            q = n // (((dp * e - 1) // i) + 1)
            phi = (q - 1) * (p - 1)
            d = gp.invert(e, phi)
print(p)
print(q)
```

然后就会输出p、q，再把p、q放到rsatool生成der证书，用openssl转成pem（大佬轻点喷，我只会这么用www

```
 > python rsatool.py -f DER -o key.der -p 167491603290232240165109588122788533113389414892381818156844128040193230978258977820405344205575296236371810427163650149605152056848232885222313353175604339541646561904247957829866027314556374355724182064112393004948463738291920723783245808179255742950559196088831263741806293908034669816429240284314008447447 -q 135614405996392828283288405736816325971158828195581321137267815028274015935746901788826424186827187305964377540945597767870885565726850264456049944775721936464833029271446916299066431842045054106684672619067404844022080815572204158632860297345943545872303196205961279815313762145298097712015966260328367919427
```

```
 > openssl rsa -inform DER -outform PEM -in key.der -out mykey.pem
writing RSA key
```

这时生成的mykey.pem就是正确的密钥，开始解密

这里又踩了一个坑，openssl解密死活不成功，结果用cyberchef一次就成功了，挺奇怪的（用open file as input）

![image](/assets/cnblogs/春秋杯冬季赛-EzMisc WP/3539156-20250119184634872-460928737.png)


这样就获得了压缩包密码

### 3、图片解密

提示 2、图片经过了Arnold变换（不给提示真的有人知道吗

在网上搜索这个变换，找到一个可用的代码，自己改了一下让他能把图片输出

[-Arnold-/arnold.py at main · mouguawang/-Arnold-](https://github.com/mouguawang/-Arnold-/blob/main/arnold.py)

```python
import numpy as np
import cv2
import random


def dearnold_encode(image, a, b):
    arnold_image = np.zeros(shape=image.shape)  

    h, w = image.shape[0], image.shape[1]
    N = w  
    for x in range(h):
        for y in range(w):
            new_x = ((a * b + 1) * x - a * y) % N
            new_y = (-b * x + y) % N
            arnold_image[new_x, new_y, :] = image[x, y, :]

    arnold_image = np.uint8(arnold_image)

    return arnold_image



cishu=0
for _ in range(10000):
     r = cv2.imread('flag.png')
    a=random.randint(1,1000)
    b=random.randint(1,1000)
    cishu+=1
    r = dearnold_encode(r, a, b)
    cv2.imwrite("D:\\hi\\" + "{}.png".format(cishu), r)

```
提示：opencv和numpy不兼容错误可以试试用python3.8（我的在虚拟机里面跑的）

这里纯随机，我开了八个Python强制多线程输出了几万张图片，花了一个小时去找，偶然间发现了最靓的仔
参数a=192,b=656

（其实这个也不是完美的，但是已经没办法了，只有这个是能看到内容的）
这里可以把图片缩小看得更清楚

![image](/assets/cnblogs/春秋杯冬季赛-EzMisc WP/3539156-20250119184602132-1326876351.png)


通过我的反复查看和大胆的蒙，花了一个小时终于把flag弄出来了，挺不容易的QAQ

flag{3089ea1c-23a0-4889-a87f-daabe2f6e1b4}
