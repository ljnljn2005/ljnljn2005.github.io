---
title: "APK取证分析"
date: 2026-02-28 12:02:00
categories:
  - "Others"
tags:
  - "Reverse"
cnblogs_postid: "19651888"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/19651888"
---

> 来自培训资料，侵权请联系我删除，谢谢！

通过抓包应用，迅速定位和程序有关的域名和 ip 地址。
通过常用脱壳工具，轻松脱掉市面上大多数加壳。
通过绕检测工具，辅助我们使用虚拟机调试 APP 应用。
通过算法助手，轻松迅速的破解加密内容。
## 抓包工具
### 安卓上安装的
**Packet Capture**
无 Root 抓包，利用 packet capture 证书。
使用中间人技术对 SSL 解密。
显示文本或显示 16 进制
![assets/APK取证分析/file-20260228091535947.png](/assets/cnblogs/APK取证分析/3539156-20260228154602419-1010176156.png)
**HTTP canary**
一款专注于 http 协议抓包和注入得 Android 应用。
支持对 HTTP1.0/1.1/2/HTTPS/WebSocket/TLS/SSL 等网络协议抓取和注入
支持静态注入和动态注入模式
修改请求参数、请求头、请求体、响应码、响应头和响应体等数据
1.协议类型： HTTP TCP UDP
2.相应状态：
200请求成功
301资源被永久转移到其它 URL
404请求的资源（网页等）不存在
500内部服务器错误
3.部分请求信息
![assets/APK取证分析/file-20260228091633738.png](/assets/cnblogs/APK取证分析/3539156-20260228154602645-1931013918.png)
域名
服务器：IP 地址和端口
响应码：请求是否响应
![assets/APK取证分析/file-20260228091653490.png](/assets/cnblogs/APK取证分析/3539156-20260228154602629-1910947779.png)
点击预览，查看详细的请求数据（ json 字符串格式）
![assets/APK取证分析/file-20260228091712043.png](/assets/cnblogs/APK取证分析/3539156-20260228154602628-2085646379.png)
![assets/APK取证分析/file-20260228091717917.png](/assets/cnblogs/APK取证分析/3539156-20260228154602496-21804214.png)
点击预览，查看详细的响应数据json 字符串格式）
此应用还可以解析返回数据为图片等其他格式。
![assets/APK取证分析/file-20260228091738299.png](/assets/cnblogs/APK取证分析/3539156-20260228154602663-205479727.png)
![assets/APK取证分析/file-20260228091741863.png](/assets/cnblogs/APK取证分析/3539156-20260228154602603-1595486391.png)
![assets/APK取证分析/file-20260228091744988.png](/assets/cnblogs/APK取证分析/3539156-20260228154602747-1608429870.png)
### 进阶对抗：虚拟机+HTTP canary 绕过检测
将目标APP 安装在 Vmos 虚拟机中，在 Vmos 虚拟机外对 Vmos 进行抓包

### r0capture
https://github.com/r0ysue/r0capture
无视所有证书校验或绑定；
通杀协议包括：
Http,WebSocket,Ftp,Xmpp,Imap,Smtp,Protobuf 等等、以及它们的 SSL 版本；
通杀所有应用层框架，包括 HttpUrlConnection 、Okhttp1/3/4 、 Retrofit/Volley 等等；
无视加固，不用考虑加固的事情；
（导图来自r0capture仓库）
![](assets/APK取证分析/summary2.jpg)
Spawn 模式：`python r0capture.py U f 包名 v`
Attach 模式，抓包内容保存成 pcap 文件供后续分析：`python r0capture.py U 包名 v p xxxx.pcap`
Frida连接
在真机上安装的教程：[AndroidSecurityStudy/FRIDA/A01/README.md at master · r0ysue/AndroidSecurityStudy · GitHub](https://github.com/r0ysue/AndroidSecurityStudy/blob/master/FRIDA/A01/README.md)
1.端口转发后连接 adb
adb forward tcp:27042 tcp:27042
adb shell
2.Fridaserver 目录
data/local/tmp
3.运行 Frida server
./frida server
![assets/APK取证分析/file-20260228092347237.png](/assets/cnblogs/APK取证分析/3539156-20260228154603363-981452728.png)
## 脱壳工具
### apk信息查看软件APK Messenger
包名
加固类型
权限信息
签名信息
![assets/APK取证分析/file-20260228102528634.png](/assets/cnblogs/APK取证分析/3539156-20260228154603200-1369953315.png)
### GDA（和jadx很像说是
[GDA主页-亚洲首款交互式Android反编译器](http://www.gda.wiki:9090/)
![assets/APK取证分析/file-20260228104822219.png](/assets/cnblogs/APK取证分析/3539156-20260228154603286-1164438077.png)
### 易开发
易开发是一款帮助开发人员快速开发的工具，功能包括界面分析，页面信息，加固脱壳，支持Android9.0
[GitHub - WrBug/DeveloperHelper: 易开发是一款帮助开发人员快速开发的工具，功能包括界面分析，页面信息，加固脱壳，支持Android9.0](https://github.com/WrBug/DeveloperHelper)
![assets/APK取证分析/file-20260228105717075.png](/assets/cnblogs/APK取证分析/3539156-20260228154603096-307030316.png)
数据信息：
SharedPreferences是Android 系统提供的通用的数据持久化框架，用于存储和读取 key value 类型的原始基本数据对。
SharedPreferences仅支持 boolean 、 float 、 int 、 long 和 string 等基本类型的存储。
SharedPreferences 主要用于存储系统的配置信息，类似于 Windows 下常用的 ini 文件。例如上次登录的用户名、上次最后设置的信息等，通过保存上一次用户所做的修改或者自定义参数设定，当再次启动程序后依然保持原有设置。它是用键值对的方式存储的，方便管理写入和读取。
### BlackDex
针对一（落地加载）、二（内存加载）、三（指令抽取）代壳
[GitHub - CodingGay/BlackDex: BlackDex is an Android unpack(dexdump) tool, it supports Android 5.0\~12 and need not rely to any environment. BlackDex can run on any Android mobile phone or emulator, you can unpack APK File in several seconds.](https://github.com/CodingGay/BlackDex)
![assets/APK取证分析/file-20260228113405368.png](/assets/cnblogs/APK取证分析/3539156-20260228154603269-1242234886.png)
### 反射大师
xposed 插件，支持进行安卓动态的修改，支持进行多种功能的修改。
![assets/APK取证分析/file-20260228114643005.png](/assets/cnblogs/APK取证分析/3539156-20260228154603126-1607859366.png)
### Fdex2
XPosed 的一个插件
Hook ClassLoader 的loadClass 方法，反射调用 getDex 方法取得 Dex
![assets/APK取证分析/file-20260228114648880.png](/assets/cnblogs/APK取证分析/3539156-20260228154603155-378961142.png)
## 其他工具
### 绕检测：对话框取消
除强制关闭对话框，防止被强制退出等功能，还有很多绕过检测的附加功能。
![assets/APK取证分析/file-20260228114735370.png](/assets/cnblogs/APK取证分析/3539156-20260228154603099-1974014591.png)
![assets/APK取证分析/file-20260228114738733.png](/assets/cnblogs/APK取证分析/3539156-20260228154603076-142896861.png)
### 绕检测：RootCloak
点击 manage Apps ，选择要对抗检测的包名
![assets/APK取证分析/file-20260228115040702.png](/assets/cnblogs/APK取证分析/3539156-20260228154603049-376800729.png)
![assets/APK取证分析/file-20260228115044017.png](/assets/cnblogs/APK取证分析/3539156-20260228154603106-1199728421.png)
### 绕检测：Xposed Hider
一款为 xposed 框架打造的隐藏模块，可以对 xposed 框架进行隐藏，有效地将各种应用无法检测出安装了 xposed 框架
红色为已选中
![assets/APK取证分析/file-20260228115319051.png](/assets/cnblogs/APK取证分析/3539156-20260228154603230-2082119853.png)
### 算法助手
![assets/APK取证分析/file-20260228120013803.png](/assets/cnblogs/APK取证分析/3539156-20260228154603134-241323678.png)
![assets/APK取证分析/file-20260228120017116.png](/assets/cnblogs/APK取证分析/3539156-20260228154603224-1123594452.png)
![assets/APK取证分析/file-20260228120020894.png](/assets/cnblogs/APK取证分析/3539156-20260228154603183-1065934692.png)
红色为已查看
进入后主要检查【 解密结果 】
查看调用堆栈（找到关键代码位置）
![assets/APK取证分析/file-20260228120039133.png](/assets/cnblogs/APK取证分析/3539156-20260228154603179-800747723.png)
![assets/APK取证分析/file-20260228120043221.png](/assets/cnblogs/APK取证分析/3539156-20260228154603204-827879566.png)
查看目标文件位置，可以去实际文件验证
查看调用堆栈，找到关键代码位置
![assets/APK取证分析/file-20260228120057406.png](/assets/cnblogs/APK取证分析/3539156-20260228154603207-1574774831.png)
![assets/APK取证分析/file-20260228120100512.png](/assets/cnblogs/APK取证分析/3539156-20260228154603277-493857412.png)
打开算法助手，可以看到一共有两栏，分别为应用和日志。
![assets/APK取证分析/file-20260228154832119.png](/assets/cnblogs/APK取证分析/3539156-20260228163642373-351089968.png)
点击进入后在算法分析一栏中，勾选 摘要算法、含密钥信息摘要和加密算法三项。
![assets/APK取证分析/file-20260228154844833.png](/assets/cnblogs/APK取证分析/3539156-20260228163642511-1014665645.png)
点击右上角启动调试的目标程序，程序运行后返回加密算法页面，到日志一栏就可以看到抓取到算法相关数据了
![assets/APK取证分析/file-20260228155004086.png](/assets/cnblogs/APK取证分析/3539156-20260228163642488-970392070.png)
数据详细记录了加密算法的类型、加密的原文本、解密后的文本内容。
![assets/APK取证分析/file-20260228155015893.png](/assets/cnblogs/APK取证分析/3539156-20260228163642349-362046267.png)
### 扩展：加解密技巧
常见加密算法
线性散列算法（签名算法）MD5
对称性加密算法AES DES DESede
非对称性加密算法RSA
MD5是一种被广泛使用的线性散列算法，可以产生出一个 128 位（ 16 字节）的散列值（ hash value ），用于确保信息传输完整的一致性。且 MD5 加密之后产生的是一个固定长度（ 32 位或 16 位）的数据。
常规讲MD5 是不存在解密的。但是理论上 MD5 是可以进行反向暴力破解的。暴力破解的大致原理就是用很多不同的数据进行加密后跟已有的加密数据进行对比，由此来寻找规律。理论上只要数据量足够庞大 MD5 是可以被破解的。但是要注意，破解 MD5 是需要考虑破解的成本（时间和机器性能）。
MD5增加破解难度
使用一段无意义且随机的私匙进行MD5 加密会生成一个加密串，我们暂且称之为串 1
将要加密的的数据跟串1 拼接，再进行一次 MD5 ，这时会生成串 2
将串2 再次进行 MD5 加密，这时生成的串 3 就是我们加密后的数据。
DES全称为 Data Encryption Standard ，即数据加密标准是一种使用密钥加密的算法。该加密算法是一种对称加密方式，其加密运算、解密运算需要使用的是同样的密钥（一组字符串）即可。
![assets/APK取证分析/file-20260228163328339.png](/assets/cnblogs/APK取证分析/3539156-20260228163642357-998809869.png)
现在用
AES 这个标准来替代原先的 DES 。
AES和 DES 的区别：
加密后密文长度的不同
DES加密后密文长度是 8 的整数倍
AES加密后密文长度是 16 的整数倍
应用场景的不同
企业级开发使用DES 足够安全
如果要求高使用AES
DES和 AES 切换只需要修改 CryptoJS.AES <=> CryptoJS.DES
使用DES/AES 进行数据交互时要求双方都拥有相同的私匙
DES算法的入口参数有三个：Key、 Data 、 Mode padding 。
Key为 7 个字节共 56 位，是 DES 算法的工作密钥；
Data为 8 个字节 64 位，是要被加密或被解密的数据；
Mode为 DES 的工作方式。
padding为填充模式，如果加密后密文长度如果达不到指定整数倍（ 8 个字节、16 个字节），填充对应字符padding的赋值固定为 CryptoJS.pad.Pkcs7 即可
DESede是针对 DES 密钥长度偏短和迭代次数偏少等问题做了相应改进，提高了安全强度。
DESede算法将密钥长度增加至 112 位或 168 位，抗穷举攻击能力显著增强，但核心仍是 DES 算法，虽然通过增加迭代次数提高了安全性，但同时也造成了处理速度较慢，密钥计算时间加长，加密效率不高等问题。
![assets/APK取证分析/file-20260228163419690.png](/assets/cnblogs/APK取证分析/3539156-20260228163642258-1571339579.png)
RSA加密算法是一种非对称加密算法。在公开密钥加密和电子商业中RSA 被广泛使用。
非对称加密算法：
非对称加密算法需要两个密钥：公开密钥（publickey 简称公钥）私有密钥（privatekey 简称私钥）
公钥与私钥是一对，如果用公钥对数据进行加密，只有用对应的私钥才能解密。
因为加密和解密使用的是两个不同的密钥，所以这种算法叫作非对称加密算法。

#### Md5技巧
java.security.MessageDigest 类用于为应用程序提供信息摘要算法的功能，如 MD5 或 SHA 算法。简单点说就是用于生成散列码。
搜索大法：关键词MD5
https://www.somd5.com/
https://cmd5.com/
彩虹表：[转 （总结）密码破解之王：Ophcrack彩虹表(Rainbow Tables)原理详解（附：120G彩虹表下载）-腾讯云开发者社区-腾讯云](https://cloud.tencent.com/developer/article/1556318)
加盐（salt）
#### AES/DES技巧
Cipher对象中 Cipher.getInstance创建密匙主要使用SecretKeySpec 、 KeyGenerator 和KeyPairGenerator 三个类来创建密匙
https://www.mklab.cn/utils/aes
搜索大法：字符串AES/DES
![assets/APK取证分析/file-20260228162620368.png](/assets/cnblogs/APK取证分析/3539156-20260228163642412-1655429554.png)
#### Base64伪加密
Base64是一种用 64 个字符来表示任意二进制数据的方法。base64 是一种编码方式而不是加密算法。只是看上去像是加密而已。
https://base64.us/
