---
title: "使用已知的p、q生成私钥解rsa密文的方法"
date: 2025-01-01 07:08:00
categories:
  - "CTF Writeup"
tags:
  - "CTF"
  - "Writeup"
  - "Crypto"
cnblogs_postid: "18645214"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18645214"
---

> 昨天渗透赛的一道题，研究了一下颇有感触，给大家分享一下（2024年的最后一天还要坐牢呜呜呜）

先用rsatool根据已知的p、q生成公钥

```
python rsatool.py -f DER -o key.der -p 31764044218067306492147889531461768510318119973238219147743625781223517377940974553025619071173628007991575510570365772185728567874710285810316184852553098753128108078975486635418847058797903708712720921754985829347790065080083720032152368134209675749929875336343905922553986957365581428234650288535216460326756576870072581658391409039992017661511831846885941769553385318452234212849064725733948770687309835172939447056526911787218396603271670163178681907015237200091850112165224511738788059683289680749377500422958532725487208309848648092125981780476161201616645007489243158529515899301932222796981293281482590413681 -q 19935965463251204093790728630387918548913200711797328676820417414861331435109809773835504522004547179742451417443447941411851982452178390931131018648260880134788113098629170784876904104322308416089636533044499374973277839771616505181221794837479001656285339681656874034743331472071702858650617822101028852441234915319854953097530971129078751008161174490025795476490498225822900160824277065484345528878744325480894129738333972010830499621263685185404636669845444451217075393389824619014562344105122537381743633355312869522701477652030663877906141024174678002699020634123988360384365275976070300277866252980082349473657
```

然后使用Win64OpenSSL转公钥文件为pem

```
openssl rsa -inform DER -outform PEM -in key.der -out mykey.pem
```

获得pem后直接打开，把私钥复制下来

然后使用以下Python脚本解密

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import base64

# 假设你的私钥PEM文件名为'private_key.pem'
pem_private_key = b"""
-----BEGIN PRIVATE KEY-----

-----END PRIVATE KEY-----
"""

# 从PEM文件加载私钥
private_key = serialization.load_pem_private_key(
    pem_private_key,
    password=None,  # 如果你的私钥是加密的，这里需要提供密码
    backend=default_backend()
)

# 假设你已经有了加密后的密文（这里用base64编码的字符串表示）
ciphertext_b64 = "..."  # 将这里的"..."替换为你的密文（base64编码）

# 将base64编码的密文解码为二进制数据
ciphertext = base64.b64decode(ciphertext_b64)

# 使用私钥解密密文
# 注意：你需要确保解密时使用的填充方式与加密时使用的填充方式相同
try:
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    #print(f'Decrypted message: {plaintext.decode("utf-8")}')
    decoded_bytes = base64.b64decode(plaintext.decode("utf-8").encode('utf-8'))
    decoded_str = decoded_bytes.decode('utf-8')
    print(decoded_str)
except Exception as e:
    print(f'An error occurred during decryption: {e}')
```

运行后可以得到解密后的密文
![image](/assets/cnblogs/使用已知的p、q生成私钥解rsa密文的方法/3539156-20250101070706786-2073177158.png)
