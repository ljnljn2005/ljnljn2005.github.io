---
title: "学校CTF纳新赛WP"
date: 2024-11-23 20:41:00
categories:
  - "CTF Writeup"
tags:
  - "CTF"
  - "Writeup"
cnblogs_postid: "18565042"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18565042"
---

### Misc 方向

#### 1.misc-forensics

首先用volatility2对内存镜像进行分析
![image](/assets/cnblogs/学校CTF纳新赛WP/3539156-20241123204036255-1507425932.png)

然后用Win7SP1x64进一步分析镜像。

想到flag可能藏在文件中，于是对系统文件进行扫描

发现镜像缓存中出现可疑文件flag.zip，于是将其导出

![image](/assets/cnblogs/学校CTF纳新赛WP/3539156-20241123204025503-1589784032.png)


将导出的file.None.0xfffffa80026be2c0.dat加上后缀名     
 .zip，发现压缩包需要密码才能读取里面的flag.txt文件，于是寻找密码。

从内存分析角度，决定分析账户密码

首先从镜像中获取密码

![image](/assets/cnblogs/学校CTF纳新赛WP/3539156-20241123204019500-816893315.png)


然后使用网页工具（https://hashes.com/en/decrypt/hash#/）对NTLM-HASH值逐一解码

![image](/assets/cnblogs/学校CTF纳新赛WP/3539156-20241123203958025-1246062810.png)
![image](/assets/cnblogs/学校CTF纳新赛WP/3539156-20241123204000388-1339354101.png)
![image](/assets/cnblogs/学校CTF纳新赛WP/3539156-20241123204004169-1808128460.png)


将123456和p@ssworld代入压缩包中，发现p@ssworld为压缩包密码

最后得到flag

![image](/assets/cnblogs/学校CTF纳新赛WP/3539156-20241123203945403-1443883957.png)


#### 2.happy_pvz

 首先根据提示把存档文件放进去
 ![image](/assets/cnblogs/学校CTF纳新赛WP/3539156-20241123203924786-544693333.png)


然后发现开始界面就有疑似flag的部分

![image](/assets/cnblogs/学校CTF纳新赛WP/3539156-20241123203915460-1548074011.png)


随后到处点点，发现“帮助”里面有一段flag，而且这段flag在中间 

![image](/assets/cnblogs/学校CTF纳新赛WP/3539156-20241123203911418-1454217114.png)


根据后面给的提示找到flag2

<img src="C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20241123185005510.png" alt="image-20241123185005510" style="zoom:33%;" />

 注意到可以给树施肥，所以小施一手，找到flag2部分

![image](/assets/cnblogs/学校CTF纳新赛WP/3539156-20241123203904401-863175085.png)


最后打关，因为实在太菜所以就用了修改器打

![image](/assets/cnblogs/学校CTF纳新赛WP/3539156-20241123203858180-1821518173.png)


![image](/assets/cnblogs/学校CTF纳新赛WP/3539156-20241123203855083-1306345983.png)


![image](/assets/cnblogs/学校CTF纳新赛WP/3539156-20241123203851039-1043889284.png)


僵王的三轮攻势各有一部分flag，记录下来，后来也可以看出这是flag4的内容

![image](/assets/cnblogs/学校CTF纳新赛WP/3539156-20241123203846877-2123673228.png)


最后把各组flag结合起来就是最后的flag

#### 3.签到时间到！

扫码，文章拉到最底下即可获得flag

### Pwn方向

#### ezsignin

典型linux常用指令

![image](/assets/cnblogs/学校CTF纳新赛WP/3539156-20241123203840830-838343825.png)


### Reverse方向

#### BABYPYC

一眼往Python逆向

首先exe转pyc，使用pyinstxtractor-ng

![image](/assets/cnblogs/学校CTF纳新赛WP/3539156-20241123203835026-1501423236.png)

随后在编译文件夹里提取出babypyc.pyc，再进行反编译（用pycdc转py）
![image](/assets/cnblogs/学校CTF纳新赛WP/3539156-20241123203745752-1845292412.png)
![image](/assets/cnblogs/学校CTF纳新赛WP/3539156-20241123203733666-447489775.png)


反编译后发现反编译并不完整，于是询问AI解决

```Python
# Source Generated with Decompyle++
# File: babypyc.pyc (Python 3.12)
def xor_encrypt(input_str):
    key = 'qui1t_cppuisa'
    encrypted = []
# WARNING: Decompyle incomplete

print('welcome to cppuisa')
print('flag是cppu{开头')
user_input = input('Please enter your input: ')
encrypted_input = xor_encrypt(user_input)
correct_encrypted = '\x12\x05\x19D\x0f.\x16\x19A\x016\x03\r\x14\x14\x1aT+;\x02\x19\x14\x14\x00,\x0c\x14\x08'
if encrypted_input == correct_encrypted:
    print('right')
    return None
print('注意\\r是回车0xd')
print('wrong')
```

AI给出的解密代码：

```python
def xor_encrypt(input_str):
    key = 'qui1t_cppuisa'
    encrypted = []
    for i, char in enumerate(input_str):
        encrypted.append(ord(char) ^ ord(key[i % len(key)]))
    return bytes(encrypted)

correct_encrypted = b'\x12\x05\x19D\x0f.\x16\x19A\x016\x03\r\x14\x14\x1aT+;\x02\x19\x14\x14\x00,\x0c\x14\x08'
key = 'qui1t_cppuisa'

# 尝试还原输入
possible_input = []
for i, encrypted_char in enumerate(correct_encrypted):
    possible_input.append(chr(encrypted_char ^ ord(key[i % len(key)])))

print("可能的输入（可能是flag的剩余部分）:", ''.join(possible_input))
```

最后得到flag

![image](/assets/cnblogs/学校CTF纳新赛WP/3539156-20241123203716388-1266169011.png)


### Web方向

#### web签到

发现密文，直接Cyberchef一把梭

![image](/assets/cnblogs/学校CTF纳新赛WP/3539156-20241123203650002-7948565.png)

### Crypto方向

#### 1.编码code

分开解码

```Python
from Crypto.Util.number import bytes_to_long, long_to_bytes
from base64 import b64encode, b64decode
import os
m1 = 443281125274097696282661878389435999
m2 = b'686f775f746f5f6465636f64655f74'
m3 = b'aGVzZV9jb2RlISEhISF9'
m3_decoded = b64decode(m3)
m2_hex_str = m2.decode()
m2_decoded = bytes.fromhex(m2_hex_str)
m1_decoded = long_to_bytes(m1)
with open("m0.txt", "rb") as f:
    m0 = f.read()
m0_str = m0.decode('utf-8')
m1_str = m1_decoded.decode('utf-8')
m2_str = m2_decoded.decode('utf-8')
m3_str = m3_decoded.decode('utf-8')
flag = m0_str + m1_str + m2_str + m3_str
print(flag)
```

#### 2.你有装sagemath软件并配置好了吗？
```
from Crypto.Util.number import *

[p0, p_leak] = [342786932597899774080278919233, 2180942305879083313385699688688649770575401960705813731167982873307515150902453812164540872752066006325334111444533180891136]
c = 24392936069556102540199862517997854393197282565478496250081102802183371142865451971064225168186026592356841946552737541277265864134925745973738533069500679861657429567572859664345004643629443253743567163595062976314779951347071882927361459802175502199147574036049243190969884473120604525821980294488378077910
[e, n] = [65537, 105652349991856297963642142108557236066399488308106611883979661581002804036935073512170546163478780443651826779340719652444565906473476781249870360455121578629563389144896951722671963720247303540893194705960514108348935180482952376603146943444037124147845426576841065365107576028356631911076185405777461236441]

p_low = p0 % 2**100 + p_leak

PR.<x> = PolynomialRing(Zmod(n))
f = x*2^412 + p_low
f = f.monic()
res = f.small_roots(2^100,0.49)
print(res)  



p = int(res[0]*2^412 + p_low)
q = n//p
phi = (p-1)*(q-1)
d = inverse(e, phi)
m = int(pow(c, d, n))
print(long_to_bytes(m).decode())  
```
正好电脑里有，通过shell装库后运行

![image](/assets/cnblogs/学校CTF纳新赛WP/3539156-20241123203636868-1042810329.png)


#### 3.古典入门

先改成zip文件解压，然后问AI

```python
# 已知的密钥
k1 = "<<<<<<<<<<<<<<<<SeeU2024>>>>>>>>>>>>>>>>>>>>"
k2 = 4


def decrypt_c1():
    with open("c1.txt", "rb") as f1:
        c1_encrypted = f1.read().decode()

    flag1_decrypted = ""
    for i in range(len(c1_encrypted)):
        t = chr(ord(c1_encrypted[i]) ^ ord(k1[i % len(k1)]))
        flag1_decrypted += t

    return flag1_decrypted


def decrypt_c2():
    with open("c2.txt", "rb") as f2:
        c2_encrypted = f2.read().decode()

    length_c2 = len(c2_encrypted)
    flag2_decrypted = [''] * length_c2
    for i in range(k2):
        for j in range(i, length_c2, k2):
            flag2_decrypted[j] = c2_encrypted[(j // k2) + (length_c2 // k2) * (k2 - 1 - i)]

    flag2_decrypted = ''.join(flag2_decrypted)
    return flag2_decrypted


if __name__ == "__main__":
    flag1_decrypted = decrypt_c1()
    flag2_decrypted = decrypt_c2()

    flag = flag1_decrypted + flag2_decrypted
    print(flag)
```

发现运行结果不对，于是进行分析，flag2部分解不开，flag1没有问题

![image](/assets/cnblogs/学校CTF纳新赛WP/3539156-20241123203628984-1875487033.png)


注意到源代码里有一个k2=4，猜测可能是栅栏密码

用网上工具解出flag2答案

![image](/assets/cnblogs/学校CTF纳新赛WP/3539156-20241123203600478-1768869626.png)

#### 4.baby_LCG

```Python
from Crypto.Util.number import *
from random import *
a = 1378752619434943933785591780693716018664050557123518722301140245162895768407168240162306093951546967956912779165269642352934543087254572566669599956060387
b = 2606396920116946933049611106919710556311992662089455045180948208442532420748038482818285161345472390027502315696857114200070403821911000030677455069309730
N = 8396614074175608834043974256584188896561302956276378241853443845559690162831762023481498499086684260749196385524201072401155399503345843775243288541771037
t = 3616138044023560411837659702316171418583279311144999057428090421000076027945616204165037620038343983511514237669506728220338423933986128767471891171733644
def inverse_mod(a, N):
    return inverse(a, N)
a_inv = inverse_mod(a, N)
seed = (t - b) * a_inv % N
flag = long_to_bytes(seed)
print("Flag:", flag.decode())
```

运行代码获得flag

![image](/assets/cnblogs/学校CTF纳新赛WP/3539156-20241123203534424-580971538.png)


#### 5.RSA_baby_to_EZ

flag1用AI解决

```Python
from Crypto.Util.number import *
from gmpy2 import *
e1 = 46273
n1 = 85149570318873397545858079769801747450955741032317421776005716419879307923817534832164193613680490496899198747179647303049788793083184220527271752037270640212143211363856115525127078383954331240479800951293505781103223095879326704698309211730316889311752593547645238748228385316179656229727884957804439714433
leak1_p = 7413041528546333282980158884011567786378341098195756764620523543522445167822444906245616440118927873532694017556517597552504089137267962327881211623910649
c1 = 13267682737577234072298553007761836634855872006599433939169643193561466175233974840639113280734923882117950741744086006704115327654248899370247329393426911960661758439351132110520234301214086149622313552075784324585591251100779472720617755754518453380506866507345906649371853362101067958543959589477359832247
dp = int(invert(e1, leak1_p - 1))
m1 = pow(c1, dp, leak1_p)
flag1 = long_to_bytes(m1).decode()
print("Flag1:", flag1)
```

![image](/assets/cnblogs/学校CTF纳新赛WP/3539156-20241123203540512-50922086.png)



第二个是dp、dq泄露，用某本CTF书上的代码可以解出来

```Python
from Crypto.Util.number import *
from gmpy2 import *
leak2 = [9130952141310948270813914839164548768194568221076998554877157061550874337219340405866020045264267400572908708681520831038764240705162325675508325496370633, 11765754785716114411402094537441078398751766315315841015319990653119612632885850920215985583783664765349992133722712384540945876398088342800629916671564931, 2150611543954114376160596068541532175024110741850690594652629552572010948026328847142866870433229491837400709829533880641963725606771342882840407682660465, 11652086611223823308288391092583038539185239072274349707821865541796029774877598391672886685755362725322755678146227617119790330212874965768632388400411553]
p, q, dp, dq = leak2
c =36143891114726447171881668756030896181416980920172151819411883676429937142736099660788215446252699693685766715960803478123837069372557401384774091091748636542226732421801866559240400874059658572337841851913255119308146024808197979353538214455355578879556557165693355484549592722433455227214988918929425562270
invp = invert(p, q)
m1 = powmod(c, dp, p)
m2 = powmod(c, dq, q)
m = ((m2 - m1) * invp % q) * p + m1
print(long_to_bytes(m))
```

![image](/assets/cnblogs/学校CTF纳新赛WP/3539156-20241123203516287-1817710153.png)

```
-----BEGIN RSA PRIVATE KEY-----
MIICWwIBAAKBgEwrJqw70z7qLrmbmkUV67/WCXKjIQhBlqo7/iUcdkHXEn6AWV1R
+tf8g8KZWJBbaLcdgQnLTGyFTyMKAPlSSsikzc6srt9iOngUSNqnQLS9eeryrogx
ZKvPWkENzkC72AcxsgjHYRvSAeZCiRyXSKS1X4Qd4h4b5UzkN8KJ/l45AgMAzrcC
gYBAjrC3A8udCXSBWjnesEFih0Sli8GheeOllWdKwVASYUBibrCCMtutcHm8msHx
INuKkwUaavihhdoWh0WXeBKkYX6qKI582prnv+iunLkarF6aA8vW/6gEVCIkVgm/
Pv7I3GRohAN5S4FatrNpcLeQJe1X324TuA9e2KLR/qfJBwJBAJP2kA/VugzSSjQd
4xSePvRuY4cpZKs4YJkwfh+1UxeMdOnyvZc6rUGeJQzqquB4DyW0/yHjzxlXHjBz
hSNimPECQQCDyKoe4dS/CgHbjzHMCWHCKlR9W6VKhzmSA1P9NB1bA6UTc6I2jxNd
RvZvJYbfOqYB6Pns1n6Zajd5Y6iM8NnJAkA7ZtOmtVws2DMB8fF8xDIXPoVSdK7n
he1DBP5zdekLRdikzTzIhhmhdOzVEisT3BVZNgTy5u3aa+G84MSFgWNXAkEAgwWV
u775/7/t9uYz1gCrGM+UNdmAnVjjL8JXEZc+tw4aGbNc5pe168GP9PlidV5+lD7c
Qez2lZEz9KyyFAwhXwJAJJ6Y5/OVrjp6UsvbNegVqhWwv5NXRVVcg9qC91APQoIW
DiP3USPdeUlZbrTzZv/gC0LeYGkLq83ALkmdZzjCsg==
-----END RSA PRIVATE KEY-----
```
最后是用私钥文件解flag，在网上找到一个教程

先使用openssl解私钥文件

```
openssl rsa -pubin -text -modulus -in privatekey.pem > mima.txt
```

得到了参数
```
Private-Key: (1023 bit, 2 primes)
modulus:   n
    4c:2b:26:ac:3b:d3:3e:ea:2e:b9:9b:9a:45:15:eb:bf:d6:09:72:a3:21:08:41:96:aa:3b:fe:25:1c:76:41:d7:12:7e:80:59:5d:51:fa:d7:fc:83:c2:99:58:90:5b:68:b7:1d:81:09:cb:4c:6c:85:4f:23:0a:00:f9:52:4a:c8:a4:cd:ce:ac:ae:df:62:3a:78:14:48:da:a7:40:b4:bd:79:ea:f2:ae:88:31:64:ab:cf:5a:41:0d:ce:40:bb:d8:07:31:b2:08:c7:61:1b:d2:01:e6:42:89:1c:97:48:a4:b5:5f:84:1d:e2:1e:1b:e5:4c:e4:37:c2:89:fe:5e:39
publicExponent: 52919 (0xceb7)  e
privateExponent:   d
    40:8e:b0:b7:03:cb:9d:09:74:81:5a:39:de:b0:41:
    62:87:44:a5:8b:c1:a1:79:e3:a5:95:67:4a:c1:50:
    12:61:40:62:6e:b0:82:32:db:ad:70:79:bc:9a:c1:
    f1:20:db:8a:93:05:1a:6a:f8:a1:85:da:16:87:45:
    97:78:12:a4:61:7e:aa:28:8e:7c:da:9a:e7:bf:e8:
    ae:9c:b9:1a:ac:5e:9a:03:cb:d6:ff:a8:04:54:22:
    24:56:09:bf:3e:fe:c8:dc:64:68:84:03:79:4b:81:
    5a:b6:b3:69:70:b7:90:25:ed:57:df:6e:13:b8:0f:
    5e:d8:a2:d1:fe:a7:c9:07
prime1:   p
    00:93:f6:90:0f:d5:ba:0c:d2:4a:34:1d:e3:14:9e:
    3e:f4:6e:63:87:29:64:ab:38:60:99:30:7e:1f:b5:
    53:17:8c:74:e9:f2:bd:97:3a:ad:41:9e:25:0c:ea:
    aa:e0:78:0f:25:b4:ff:21:e3:cf:19:57:1e:30:73:
    85:23:62:98:f1
prime2:   q
    00:83:c8:aa:1e:e1:d4:bf:0a:01:db:8f:31:cc:09:
    61:c2:2a:54:7d:5b:a5:4a:87:39:92:03:53:fd:34:
    1d:5b:03:a5:13:73:a2:36:8f:13:5d:46:f6:6f:25:
    86:df:3a:a6:01:e8:f9:ec:d6:7e:99:6a:37:79:63:
    a8:8c:f0:d9:c9
exponent1:   dp
    3b:66:d3:a6:b5:5c:2c:d8:33:01:f1:f1:7c:c4:32:
    17:3e:85:52:74:ae:e7:85:ed:43:04:fe:73:75:e9:
    0b:45:d8:a4:cd:3c:c8:86:19:a1:74:ec:d5:12:2b:
    13:dc:15:59:36:04:f2:e6:ed:da:6b:e1:bc:e0:c4:
    85:81:63:57
exponent2:   dq
    00:83:05:95:bb:be:f9:ff:bf:ed:f6:e6:33:d6:00:
    ab:18:cf:94:35:d9:80:9d:58:e3:2f:c2:57:11:97:
    3e:b7:0e:1a:19:b3:5c:e6:97:b5:eb:c1:8f:f4:f9:
    62:75:5e:7e:94:3e:dc:41:ec:f6:95:91:33:f4:ac:
    b2:14:0c:21:5f
coefficient:
    24:9e:98:e7:f3:95:ae:3a:7a:52:cb:db:35:e8:15:
    aa:15:b0:bf:93:57:45:55:5c:83:da:82:f7:50:0f:
    42:82:16:0e:23:f7:51:23:dd:79:49:59:6e:b4:f3:
    66:ff:e0:0b:42:de:60:69:0b:ab:cd:c0:2e:49:9d:
    67:38:c2:b2
-----BEGIN PRIVATE KEY-----
MIICdQIBADANBgkqhkiG9w0BAQEFAASCAl8wggJbAgEAAoGATCsmrDvTPuouuZua
RRXrv9YJcqMhCEGWqjv+JRx2QdcSfoBZXVH61/yDwplYkFtotx2BCctMbIVPIwoA
+VJKyKTNzqyu32I6eBRI2qdAtL156vKuiDFkq89aQQ3OQLvYBzGyCMdhG9IB5kKJ
HJdIpLVfhB3iHhvlTOQ3won+XjkCAwDOtwKBgECOsLcDy50JdIFaOd6wQWKHRKWL
waF546WVZ0rBUBJhQGJusIIy261webyawfEg24qTBRpq+KGF2haHRZd4EqRhfqoo
jnzamue/6K6cuRqsXpoDy9b/qARUIiRWCb8+/sjcZGiEA3lLgVq2s2lwt5Al7Vff
bhO4D17YotH+p8kHAkEAk/aQD9W6DNJKNB3jFJ4+9G5jhylkqzhgmTB+H7VTF4x0
6fK9lzqtQZ4lDOqq4HgPJbT/IePPGVceMHOFI2KY8QJBAIPIqh7h1L8KAduPMcwJ
YcIqVH1bpUqHOZIDU/00HVsDpRNzojaPE11G9m8lht86pgHo+ezWfplqN3ljqIzw
2ckCQDtm06a1XCzYMwHx8XzEMhc+hVJ0rueF7UME/nN16QtF2KTNPMiGGaF07NUS
KxPcFVk2BPLm7dpr4bzgxIWBY1cCQQCDBZW7vvn/v+325jPWAKsYz5Q12YCdWOMv
wlcRlz63DhoZs1zml7XrwY/0+WJ1Xn6UPtxB7PaVkTP0rLIUDCFfAkAknpjn85Wu
OnpSy9s16BWqFbC/k1dFVVyD2oL3UA9CghYOI/dRI915SVlutPNm/+ALQt5gaQur
zcAuSZ1nOMKy
-----END PRIVATE KEY-----
```

再根据rsa算法原理写脚本

```Python
from Crypto.Util.number import *
from gmpy2 import *

n=0x4c2b26ac3bd33eea2eb99b9a4515ebbfd60972a321084196aa3bfe251c7641d7127e80595d51fad7fc83c29958905b68b71d8109cb4c6c854f230a00f9524ac8a4cdceacaedf623a781448daa740b4bd79eaf2ae883164abcf5a410dce40bbd80731b208c7611bd201e642891c9748a4b55f841de21e1be54ce437c289fe5e39
e=52919
d=0x408eb0b703cb9d0974815a39deb041628744a58bc1a179e3a595674ac150126140626eb08232dbad7079bc9ac1f120db8a93051a6af8a185da168745977812a4617eaa288e7cda9ae7bfe8ae9cb91aac5e9a03cbd6ffa8045422245609bf3efec8dc64688403794b815ab6b36970b79025ed57df6e13b80f5ed8a2d1fea7c907
p=0x0093f6900fd5ba0cd24a341de3149e3ef46e63872964ab386099307e1fb553178c74e9f2bd973aad419e250ceaaae0780f25b4ff21e3cf19571e307385236298f1
q=0x0083c8aa1ee1d4bf0a01db8f31cc0961c22a547d5ba54a8739920353fd341d5b03a51373a2368f135d46f66f2586df3aa601e8f9ecd67e996a377963a88cf0d9c9
dp=0x3b66d3a6b55c2cd83301f1f17cc432173e855274aee785ed4304fe7375e90b45d8a4cd3cc88619a174ecd5122b13dc15593604f2e6edda6be1bce0c485816357
dq=0x00830595bbbef9ffbfedf6e633d600ab18cf9435d9809d58e32fc25711973eb70e1a19b35ce697b5ebc18ff4f962755e7e943edc41ecf6959133f4acb2140c215f
c=31548099926009835183998137687979143238558935184182860945192515870066515610094711984467245116094654608785307629587031968930591535639282498196615401990463795178624472373143008592097060826198124211973180137608609916994588385110852393512121155308362492541751622251276383850297519887799930913433683963250133075331
n = p*q
d = invert(e, (p-1)*(q-1))
m = pow(c, d, n) # 解密
flag = long_to_bytes(m) #转文字
print(flag)
```

![image](/assets/cnblogs/学校CTF纳新赛WP/3539156-20241123203452992-1279332798.png)
