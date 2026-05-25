---
title: "盘古石WriteUp"
date: 2025-05-10 20:41:00
categories:
  - "Forensics Writeup"
tags:
  - "Forensics"
  - "Writeup"
  - "盘古石"
cnblogs_postid: "18870102"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18870102"
---

学生组109，一部分是蒙的
错了挺多，仅供记录qaq
## 手机取证

### 1.分析安卓手机检材，手机的IMSI是？[答案格式：660336842291717] Analyze the Android phone: What is the IMSI? [Answer format: 660336842291717]

460036641292715
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510200402268-1999150757.png)


### 2.养鱼诈骗投资1000，五天后收益是？[答案格式：123] Invest 1000 in "Fish farming" scam, what is return after 5 days? [Answer format: 123]

175
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510200413625-2129732662.png)


### 3.分析苹果手机检材，手机的IDFA是？[答案格式：E377D1D7-BA02-4A79-BB9A-5C2DE5BD1F17] Analyze the iPhone: What is the IDFA? [Answer format: E377D1D7-BA02-4A79-BB9A-5C2DE5BD1F17]

E477D4C7-BD02-4979-BC9D-5C5DE7BD1F17
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510200420859-1859302166.png)


### 4.Telegram应用的卸载时间是？[答案格式：2023-01-22-17:37:50] When was uninstall time of Telegram App? [Answer format: 2023-01-22-17:37:50]

2025/04/17-10:51:39
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510200427502-757967949.png)


### 5.机主hotmail邮箱地址是？[答案格式：123345@hotmail.com] What is the user’s Hotmail email address? [Answer format: 123345@hotmail.com]

xtest901234@hotmail.com
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510200433124-954780813.png)


### 6.苹果电脑开机密码是？[答案格式：12345] What is the mac’s power-on password? [Answer format: 12345]

12345678
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510200438019-876509747.png)


### 7.Telegram加密通讯中，加密聊天信息用到的第二个解密载体是？[答案格式：123.zip] The second decryption vector used to encrypt chat messages in Telegram encrypted messaging is? [Answer format: 123.zip]

### 8.贾韦码的内部代号是？[答案格式：77] What is Jia Wei Ma(贾韦码)’s internal code name? [Answer format: 77]

48
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510200444905-1321855770.png)


### 9.特快专递的收货地址是？[标准格式：老牛市快速路11号ADE公司] What is the delivery address for the express package? [Answer format: 老牛市快速路11号ADE公司]

西红市中山路35号PGS健身房
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510200450447-9469986.png)


## APK取证

### 1.分析安卓检材，远控工具包名是？[标准格式：com.app.cpp] Analyze the Android device: What is the package name of the remote control tool? [Answer format: com.app.cpp]

![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510200456457-793076853.png)

![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510200501107-2142884542.png)


### 2.远控工具中继服务器IP是？[标准格式：192.168.11.11] What is the IP of the relay server in the remote control tool? [Answer format: 192.168.11.11]

找到镜像中的数据
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510200508028-1603256049.png)

用镜像data进行替换
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510200516267-622403213.png)

打开软件
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510200522320-1747963808.png)

59.110.10.229

### 3.远控工具ID服务器端口是？[标准格式：8088] What is the “ID server”‘s open port in the remote control tool? [Answer format: 8088]

如上题
21116

### 4.远控工具中继服务器Key是？[标准格式：HoTwGxUuV9OxSSEWRFsr1DVxQBkbbFRe0ImYMTlzyec=] What is the relay server key in the remote control tool? [Answer format: HoTwGxUuV9OxSSEWRFsr1DVxQBkbbFRe0ImYMTlzyec=]

如上题
WIUqzRq1Ocx4QNnsF26dZQijKdyd2L9OfaT55hDlQCI=

### 5.远控工具中收藏的远程ID是？[标准格式：123456] What is the saved remote ID in the remote control tool? [Answer format: 123456]

![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510200530299-1537340782.png)


### 6.远程控制该手机的手机型号是？[标准格式：huawei-Hot] What is the model of the phone controlling this phone? [Answer format: huawei-Hot]

如上图
google-Pixel

### 7.监听工具包名是？[标准格式：com.app.cpp] What is the package name of the eavesdropping tool? [Answer format: com.app.cpp]

com.example.liekai可疑
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510200536916-299822833.png)

打开之后读取权限与所述题目相符
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510200543047-844268591.png)


### 8.监听工具代码主入口是？[标准格式：com.app.cpp.MainActidddy] What is the main entry point in the eavesdropping tool’s code? [Answer format: com.app.cpp.MainActidddy]

com.example.liekai.MainActivity
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510200557331-480927925.png)


### 9.监听工具的签名算法是？[标准格式：AES123RSA ] What signing algorithm does the eavesdropping tool use? [Answer format: AES123RSA]

SHA256RSA
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203311156-62317975.png)


### 10.监听工具运行多少秒后会跳转成黑色幕布？[标准格式：3.000] How many seconds after running does the eavesdropping tool display a black screen? [Answer format: 3.000]

1.000
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203318113-1428586263.png)


### 14.监听工具保存文件存储路径的数据库名称是？[标准格式：sqlite.db] What is the database name storing file paths in the eavesdropping tool? [Answer format: sqlite.db]

![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203325430-1215346940.png)


### 15.监听工具保存录像文件的文件夹是？[标准格式：file] What folder stores the eavesdropping tool’s video files? [Answer format: file]

video
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203330924-1311717874.png)


### 16.监听工具数据库中保存音视频文件的路径使用什么加密？[标准格式：Rsa] What encryption algorithm is used for the paths of audio and video files saved in the eavesdropping tool’s database? [Answer format: Rsa]

![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203336293-1459407442.png)


## 计算机取证

### 1.分析贾韦码计算机检材，计算机系统Build版本为？【标准格式：19000】 Analyze Jia Wei Ma(贾韦码)’s computer sample: What is the system Build number? [Answer format: 19000]

### 1.分析贾韦码计算机检材，计算机系统Build版本为？【标准格式：19000】 Analyze Jia Wei Ma(贾韦码)’s computer sample: What is the system Build number? [Answer format: 19000]

![[Pasted image 20250510131933.png]]
18362

### 2.计算机最后一次正常关机的时间为？UTC +0【标准格式：2025-05-06 09:00:00】 When was the computer last shut down normally (UTC +0)? [Answer format: 2025-05-06 09:00:00]

![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203342851-1622509992.png)

2025-04-18 11:20:54

### 3.计算机网卡的MAC地址为？【标准格式：00-0B-00-A0-00-00】 What is the MAC address of the computer’s network interface card? [Answer format: 00-0B-00-A0-00-00]

![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203500838-861511409.png)

00-0C-29-0F-69-00

### 4.计算机用户“贾韦码” 安全标识符SID为？【标准格式：S-X-X-X-X-X-X-X】 What is the SID of user "贾韦码"? [Answer format: S-X-X-X-X-X-X-X]

![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203506235-1673025279.png)

S-1-5-21-3733482367-3411043098-2536183883-1001

### 5.计算机默认浏览器为？【标准格式：Mozilla Firefox】 What is the default browser on the computer? [Answer example: Mozilla Firefox]

![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203511671-2017322697.png)

Google Chrome

### 6.计算机默认浏览器版本为？【标准格式：000.0.0000.00】 What is the version of the default browser? [Answer format: 000.0.0000.00]

![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203516313-1089200392.png)

135.0.7049.96

### 7.机主通过浏览器搜索国外社交软件为？【标准格式：Whatsapp】 What international social app did the owner search for? [Answer example: Whatsapp]

![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203522880-897389616.png)

telegram

### 8.机主的邮箱账号为？【标准格式：pgscup@pgs.com】 What is the owner‘s email account? [Answer format: pgscup@pgs.com]

![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203530494-1814549750.png)

tqmdavidjohnson300@gmail.com

### 9.计算机装过一款反取证软件为？【标准格式：EnCrypt.exe】 What anti-forensic software was installed on the computer? [Answer example: EnCrypt.exe]

![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203536285-259739988.png)

VeraCrypt.exe

### 10.计算机通过Xshell远程连接的ip地址为？【标准格式：127.0.0.1】 What IP address did the computer connect to via Xshell? [Answer format: 127.0.0.1]

![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203540662-1084088882.png)

192.168.56.129

### 11.机主曾买过一个美国的TG账号，请给该账号的原两步验证密码？【标准格式：8位数字】 The owner purchased an US Telegram account. Provide its original two-step verification password. [Answer format: 8 digits]

![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203544430-1514784162.png)


13770603

### 12.给出其电脑内加密容器的解密密码？【标准格式：Abc@123】 What is the decryption password for the encrypted container on the computer. [Answer format: Abc@123]

![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203549266-980917246.png)

N0tep@d++

### 13.给出其电脑内加密容器挂载的盘符？【标准格式：C】 What drive letter is assigned to the mounted encrypted container? [Answer format: C]

![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203555732-948630767.png)


![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203559657-2124093835.png)


最近访问的项目中，只有C盘和F盘，但是仿真后发现只有C盘，合理猜测F盘就是加密容器挂载的盘符

### 14.给出其电脑内存放了多少张伪造身份证？【标准格式：10】 How many forged ID cards are stored on the computer? [Answer format: 10]

在电脑中徜徉
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203605885-585097427.png)

惊喜地发现”id_cards_info“，open it
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203610507-1319661169.png)

这地址一看就是伪造的
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203617619-646415397.png)

1023

### 15.找出任敏的身份证编号？【标准格式：18位】 Find the ID number of "Ren Min(任敏)". [Answer format: 18 digits]

首先，仿真一波
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203629204-1973836676.png)

然后，在嫌疑人电脑中寻觅，偶然间发现“音乐”中有“三张表”
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203634046-641974399.png)

打开“members.csv"
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203640046-1071677197.png)

搜索”任敏“
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203643945-664202665.png)

锁定F栏”id_card“
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203648609-1811461068.png)


### 16.找出其电脑内存放的密钥文件，计算其MD5?【标准格式：字母小写】 Find the MD5 hash of the key file stored on the computer. [Answer format: lowercase letters]

在盘古石取证中找加密文件
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203739126-1107693900.png)

在虚拟机中打开，导出
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203742654-1924397706.png)

![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203746668-314042089.png)

计算MD5
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203750509-132502774.png)


### 17.找出其电脑内存放的密钥文件，解密此密钥文件，给出其内容？【标准格式：第3届pgscup】 Decrypt the key file stored on the computer and give the content. [Answer format: 第3届pgscup]


## mac

### 18.对macOS系统进行解析，登陆的电子邮件服务是谁提供的？【标准格式:pgscup】 Analyze the macOS system. Who provides the email service you log in to? [Standard format: pgscup]


### 19.系统备忘录的包名是什么？【标准格式:com.dfefef.note】 What is the package name of the system’s Notes app? [Answer format: com.dfefef.note]

![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203807566-1515889986.png)

com.apple.Notes

### 20.图片中隐藏的内容是什么？【标准格式：隐藏内容 厨子戏子痞子】 What is the hidden content in the image? [Answer format: 隐藏内容 厨子戏子痞子]
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203849758-757734133.png)
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203853804-1157776294.png)

### 21.被加密文件的扩展名是什么？【标准格式：123】 What is the file extension of the encrypted files? [Answer format: 123]

### 22.被加密的文件总共有几个？【标准格式：5】 How many encrypted files are there? [Answer format: 5]

![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203908015-1693973116.png)

7

### 23.贾韦码家使用的智能门锁品牌型号是什么？【标准格式：小米X号】 What is the brand and model of the smart lock used in Jia Wei Ma(贾韦码)’s home? [Answer example: 小米X号]

## EXE取证

### 1.分析Windows木马，其控制端ip是？[标准格式：192.168.1.11] Analyze the Windows trojan virus: What is its controller IP? [Answer format: 192.168.1.11]

104.18.45.79
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203925256-989356915.png)
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203928055-163032147.png)
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203931185-885977737.png)

### 2.软件会复制自身到哪个文件夹下？[标准格式：DaTa] Which folder does the malware copy itself to? [Answer format: DaTa]

![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203934602-1417361402.png)

### 3.接上题，复制后软件名称是？[标准格式：AppTmp.exe] Continuing last question, What is the copied filename? [Answer format: AppTmp.exe]

如上
BwAcr.exe

### 4.软件一共可以窃取多少种浏览器的信息？[标准格式：3] How many types of browsers can the malware extract data from? [Answer format: 3]

4

### 5.软件查询安装的杀毒软件出错或异常会返回什么字符串？[标准格式：Apps] What error message is returned when the malware fails to detect antivirus software? [Answer format: Apps]

## 物联网取证

### 1.分析冰箱，请问智能冰箱的品牌？【标准格式:xiaomi】 Analyze the smart refrigerator: What is its brand? [Answer format: xiaomi]

Panasonic
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203940888-1694079734.png)

### 2.请问智能冰箱的型号？【标准格式:MiFridge2024】 What is the model of the smart refrigerator? [Answer format: MiFridge2024]

图如上
模糊搜索
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203946375-1645118635.png)

### 4.请问智能冰箱默认保存几张图片？【标准格式：1】 How many images are saved by default in the smart refrigerator? [Answer format: 1]

图如下，只有四张

### 5.请问冰箱中已存的第一张图片上的内容是什么？【标准格式：满城尽带黄金甲】 What is the content of the first saved image? [Answer format: 满城尽带黄金甲]

盘古石杯贾韦码
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203952059-20136119.png)

### 8.请找出冰箱中嫌疑人图片MD5值的后六位？【标准格式：1a2b3d】 What are the last six chars of the MD5 hash for the suspect’s image in the refrigerator? [Answer format: 1a2b3d]

882564
![image](/assets/cnblogs/盘古石WriteUp/3539156-20250510203959803-280399774.png)



## 数据分析

### 1.对贾韦码计算机检材进行解析，该诈骗集团的最高层领导者的id 和姓名？【标准格式:M000001 姓名】 Analyze Jia Wei Ma(贾韦码)’s computer: Provide the ID and name of the scam group’s top leader. [Answer format: M000001 Name]



### 2.找出最高领导的所有下线中提现总额最高的成员ID？【标准格式:M0000001】 Find the ID of the member with the highest withdrawal amount among all subordinates of the top leader.. [Answer format: M0000001]


### 3.找出从直接下线获得平均佣金最高的成员ID及其平均佣金金额？【标准格式：M0000001,123.12】 Find the member ID and their average commission amount from direct referrals, where the average is the highest. [Answer format: M0000001,123.12]


### 4.找出注册时间最早的前 10% 成员中，交易次数最少的 5 位成员的 id？【标准格式：M000001,M000002,M000003,M000004,M000005】 List IDs of the 5 least active members among the earliest 10% registered user. [Answer format: M000001,M000002,M000003,M000004,M000005]



### 5.找出交易次数增长率最高的成员ID及其增长率？【标准格式：M000001,24.44%】 Find the member ID with the highest transaction growth rate and calculate their growth rate. [Answer format: M000001,24.44%]



### 6.统计状态 'active'、90天无交易、历史交易额前20%的成员数？【标准格式：111】 Count active members, no transactions in 90 days, top 20% by total transaction amount. [Answer format: 111]

### 7.找出有上线且直接下线最多的成员ID及下线数？【标准格式：M000001:数量】 Find the member ID with the most direct subordinates who also has an upline.? [Answer format: M000001:Count]



### 8.比较最早年份Q1与Q4注册成员的总交易额，指出哪个更高及具体金额？【标准格式：Q1:123.12】 Compare Q1 vs Q4 total transactions in the earliest year. Indicate which is higher and the amount. [Answer example: Q1:123.12]



### 9.找出成员地址中最常出现的省份，并计算居住在该省份的所有成员的总提现金额？【标准格式：省份,123.12】 Find the most common province in member addresses and calculate its total withdrawals. [Answer format: Province,123.12]


### 10.计算最高层领导者的净资金流？【标准格式：123.12】 Calculate the financial flow for the top leader. [Answer Format: 123.12]
