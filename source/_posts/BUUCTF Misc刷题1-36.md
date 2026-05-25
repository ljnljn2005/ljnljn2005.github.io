---
title: "BUUCTF Misc刷题1-36"
date: 2024-12-31 10:42:00
categories:
  - "CTF Misc"
tags:
  - "CTF"
  - "Misc"
  - "BUUCTF"
cnblogs_postid: "18643454"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18643454"
---

## 1、签到
flag{buu_ctf}
## 2、金三胖
gif文件先看帧
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231091256891-1900736327.png)
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231091312797-1510942614.png)
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231091331887-769612392.png)
## 3、你竟然赶我走
随波逐流一把梭
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231091447012-1465586466.png)
## 4、二维码
扫了之后发现不是flag
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231091552237-1927687561.png)
binwalk分析发现里面有压缩包
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231091649315-694474595.png)
打开压缩包后文件里提示密码是4个数字，所以直接爆破
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231091849225-1584831099.png)
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231091916252-395511018.png)
获得flag
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231091946461-113716381.png)
## 5、大白
用随波逐流
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231092041691-1766924926.png)
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231092110749-1903515249.png)
## 6、wireshark
NetA一把梭
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231092341858-736216273.png)
## 7、乌镇峰会种图
随波逐流一把梭
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231092449123-1740143526.png)
## 8、N种方法解决
随波逐流
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231092551164-684270681.png)
扫二维码获得flag
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231092659310-1899542246.png)
## 9、基础破解
提示了是4位数字密码直接爆破
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231092745925-1674816103.png)
Zmxh一眼base64加密flag，直接解码
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231092839163-1410059386.png)
## 10、文件中的秘密
flag在exif信息中
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231092948705-201231353.png)
## 11、zip伪加密
修复伪加密获得flag
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231093057364-1415844124.png)
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231093126101-47567056.png)
## 12、LSB
Stegsolve提取数据
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231093905230-2103795203.png)
一眼png，导出
扫二维码获得flag
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231094120051-154360959.png)
## 13、被嗅探的流量
NetA
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231094217358-367154773.png)
## 14、rar
爆破
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231094422687-1711880637.png)
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231094440898-1849382492.png)
## 15、qr
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231094511608-1678496813.png)

## 16、镜子里面的世界
LSB提取数据
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231094647936-573251214.png)

## 17、爱因斯坦
binwalk提取文件
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231094734778-1901416354.png)
发现压缩包要密码，看exif
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231094953265-927400205.png)
把这个输进去打开压缩包
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231095140667-1437608979.png)
## 18、ningen
binwalk提取再爆破
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231095306223-1368250180.png)
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231095354837-724819154.png)
## 19、小明的保险箱
跟上道题一模一样
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231095607804-1659011417.png)
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231095632037-821914857.png)
## 20、easycap
右键追踪流
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231095806286-652094260.png)
## 21、隐藏的钥匙
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231095958407-1945258068.png)
用010找到位置
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231100013668-1664702639.png)
复制再解码
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231100029404-136080853.png)
## 22、另外一个世界
发现后面有串二进制
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231100259882-1810628282.png)
Cyberchef From Binary
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231100355113-1820429664.png)
## 23、数据包中的线索
追踪流7发现一串base64很长，猜测是图片
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231100645547-382517918.png)
用base64转图片获得flag
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231100707709-2076861168.png)
## 24、神秘龙卷风
先爆破
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231100817479-1227552591.png)
发现是brainfuck编码，解密
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231101124724-519765805.png)
## 25、FLAG
LSB隐写，发现是压缩包
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231101256348-1671667281.png)
打开文件后疑似是elf文件，在linux打开试试
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231101522902-121703595.png)
获得flag
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231101647082-1341052750.png)
## 26、假如给我三天光明
对照盲文密码表获得解压密码kmdonowg
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231102213037-341413936.png)
打开后一眼摩斯密码
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231102335288-474542931.png)
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231102426395-1575958204.png)
解密

-.-. - ..-. .-- .--. . .. ----- ---.. --... ...-- ..--- ..--.. ..--- ...-- -.. --..


![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231102432195-261442585.png)
最后去掉CTF再转小写就是flag
flag{wpei08732?23dz}

## 27、后门查杀
先用D盾扫webshell（其实解压的时候火绒一下子扫出来了）
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231090940021-614384511.png)

找到后看这个木马
搜pass获得密码
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231090928802-998680993.png)

## 28、webshell后门
和上一题同理
先用D盾扫webshell（其实解压的时候火绒一下子扫出来了）
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231090532987-136995499.png)
找到后看这个木马
搜pass获得密码
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231090625039-1535722014.png)
## 29、来首歌吧
上面一眼摩斯密码
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231102806965-261281220.png)
..... -... -.-. ----. ..--- ..... -.... ....- ----. -.-. -... ----- .---- ---.. ---.. ..-. ..... ..--- . -.... .---- --... -.. --... ----- ----. ..--- ----. .---- ----. .---- -.-.
解密
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231102903899-1988043715.png)
发现压缩包是伪加密于是修复
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231103507085-40082801.png)
第一部分还是brainfuck
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231103650903-1037851507.png)
第二部分用diskgenius解压没有有效信息
但是在kali里解压就有（好神奇
```
7z x flag.vmdk -o./
```
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231104022676-352790707.png)
多出来一个全是ook的文件
解码
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231104132308-232887798.png)
再和上面组合获得flag
## 30、荷兰宽带数据泄露
用Routerpassview这个软件打开
下载链接：https://www.52pojie.cn/thread-1033185-1-1.html
把Username的值交上去就是答案
（这道题是真抽象）
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231144551262-1241672920.png)
## 31、九连环
图片里有压缩包，用binwalk提取
压缩包是伪加密，用随波逐流修复
随后出现一张图片和一个加密压缩包，很明显图片里藏了东西
经过反复尝试，最终是steghide隐写
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231145427735-842028330.png)
这里不用输密码就可以解开
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231145501313-2005281268.png)
解压后获得flag
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231145541131-38405855.png)
## 32、[BJDCTF2020]认真你就输了
打开表格显示文件损坏，推测表格里藏了东西
直接解压后搜索flag
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231145941724-1710111476.png)
## 33、被劫持的神秘礼物
追踪tcp流，流0里就有账号密码
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231150257286-710938660.png)
然后加密
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231150312123-1722856002.png)
## 34、被偷走的文件
NetA发现flag.rar文件
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231150653292-1559527953.png)
于是过滤TCP流，在流4发现疑似rar文件，于是导出
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231150733913-582049547.png)
导出后该压缩包有密码，考虑爆破
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231150904830-1420793277.png)
打开txt获得flag
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231151004860-1541391529.png)
## 35、[BJDCTF2020]藏藏藏
随波逐流打开图片发现是图片头zip尾，用binwalk提取失败，后来用foremost提取成功
打开提取出的压缩包有zip文件，zip里的文档打开是个二维码
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231151304856-1021570175.png)
扫描即可获得flag
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231151332869-136416130.png)
## 36、[GXYCTF2019]佛系青年
压缩包是伪加密
修复后打开fo.txt，找到下面的佛曰
遮等諳勝能礙皤藐哆娑梵迦侄羅哆迦梵者梵楞蘇涅侄室實真缽朋能。奢怛俱道怯都諳怖梵尼怯一罰心缽謹缽薩苦奢夢怯帝梵遠朋陀諳陀穆諳所呐知涅侄以薩怯想夷奢醯數羅怯諸
用随波逐流解密获得flag
![image](/assets/cnblogs/BUUCTF Misc刷题1-36/3539156-20241231151712522-1777317436.png)
