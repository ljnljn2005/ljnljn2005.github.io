---
title: "每日n题-BUUCTF密码学1-21"
date: 2025-01-04 20:17:00
categories:
  - "CTF Writeup"
tags:
  - "CTF"
  - "Writeup"
  - "BUUCTF"
  - "Misc"
  - "Crypto"
cnblogs_postid: "18652363"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18652363"
---

## 1、一眼就解密
Cyberchef Magic方法
flag{THE_FLAG_OF_THIS_STRING}
## 2、MD5
https://www.cmd5.com/
![image](/assets/cnblogs/每日n题-BUUCTF密码学1-21/3539156-20250104194522505-1057305367.png)
flag{admin1}
## 3、Url编码
![image](/assets/cnblogs/每日n题-BUUCTF密码学1-21/3539156-20250104194618259-1238616083.png)
flag{and 1=1}
## 4、看我回旋踢
看到synt想rot13（对应flag）
![image](/assets/cnblogs/每日n题-BUUCTF密码学1-21/3539156-20250104194756381-1751430954.png)
flag{5cd1004d-86a5-46d8-b720-beb5ba0417e1}
## 5、摩丝
解莫斯密码（随波逐流）
![image](/assets/cnblogs/每日n题-BUUCTF密码学1-21/3539156-20250104194932841-231281090.png)
ILOVEYOU
## 6、password
注意到key{}中长度为10，猜测可能是 “姓名缩写”＋“生日”
姓名缩写：张三——>zs
生日：19900315
“姓名缩写”＋“生日” = zs19900315
flag{zs19900315}
## 7、变异凯撒
随波逐流
![image](/assets/cnblogs/每日n题-BUUCTF密码学1-21/3539156-20250104195208738-2088259864.png)
flag{Caesar_variation}
## 8、Quoted-printable
cyberchef magic（显示的是乱码，可能是中文编码问题）
![image](/assets/cnblogs/每日n题-BUUCTF密码学1-21/3539156-20250104195258417-2064013690.png)
## 9、篱笆墙的影子
篱笆——栅栏，推测是栅栏密码
随波逐流解
![image](/assets/cnblogs/每日n题-BUUCTF密码学1-21/3539156-20250104195402865-1721093651.png)
flag{wethinkwehavetheflag}
## 10、Rabbit
Rabbit加密方法
https://www.sojson.com/encrypt_rabbit.html
![image](/assets/cnblogs/每日n题-BUUCTF密码学1-21/3539156-20250104195623452-1916741960.png)
## 11、RSA
用rsatools
![image](/assets/cnblogs/每日n题-BUUCTF密码学1-21/3539156-20250104195754527-1220928355.png)
flag{125631357777427553}
## 12、丢失的MD5
只给了这串代码说明答案藏在代码里
发现无法直接运行，丢给AI得到正确代码
```
import hashlib


def main():
    found = False
    for i in range(32, 127):
        for j in range(32, 127):
            for k in range(32, 127):
                input_str = f'TASC{chr(i)}O3RJMV{chr(j)}WDJKX{chr(k)}ZM'
                m = hashlib.md5(input_str.encode())
                des = m.hexdigest()
                if 'e9032' in des and 'da' in des and '911513' in des:
                    print(des)
                    found = True
                    break
            if found:
                break
        if found:
            break


if __name__ == "__main__":
    main()
```
运行后获得flag
flag{e9032994dabac08080091151380478a2}
## 13、Alice与Bob
https://factordb.com/index.php?query=98554799767
![image](/assets/cnblogs/每日n题-BUUCTF密码学1-21/3539156-20250104200057811-481846330.png)
flag{d450209323a847c8d01c6be47c81811a}
## 14、大帝的密码武器
在model13出现有意义的单词
![image](/assets/cnblogs/每日n题-BUUCTF密码学1-21/3539156-20250104200301528-867784364.png)
所以加密时保持一致就行
flag{PbzrPuvan}
## 15、rsarsa
rsatools
![image](/assets/cnblogs/每日n题-BUUCTF密码学1-21/3539156-20250104200558127-941788192.png)
int值即为flag
flag{5577446633554466577768879988}
## 16、Windows系统密码
https://hashes.com/en/decrypt/hash
![image](/assets/cnblogs/每日n题-BUUCTF密码学1-21/3539156-20250104200754107-1548244690.png)
## 17、信息化时代的步伐
是中文电报码
https://www.qqxiuzi.cn/bianma/dianbao.php
![image](/assets/cnblogs/每日n题-BUUCTF密码学1-21/3539156-20250104201004473-147297753.png)
flag{计算机要从娃娃抓起}
## 18、凯撒？替换？呵呵!
https://quipqiup.com/
下面线索写好MTHJ=FLAG
![image](/assets/cnblogs/每日n题-BUUCTF密码学1-21/3539156-20250104201126465-992457600.png)
下面把空格删掉加大括号就是flag
## 19、萌萌哒的八戒
图片下面是猪圈密码
![image](/assets/cnblogs/每日n题-BUUCTF密码学1-21/3539156-20250104201354389-2040894571.png)

flag{whenthepigwanttoeat}
## 20、权限获得第一步
一眼hash
https://hashes.com/en/decrypt/hash
![image](/assets/cnblogs/每日n题-BUUCTF密码学1-21/3539156-20250104201511083-1251692044.png)
flag{3617656}
## 21、RSA1
rsatools
![image](/assets/cnblogs/每日n题-BUUCTF密码学1-21/3539156-20250104201619635-285372674.png)
