---
title: "2024 NewStarCTF-WP"
date: 2024-10-19 21:33:00
categories:
  - "CTF Writeup"
tags:
  - "CTF"
  - "Writeup"
  - "NewStarCTF"
cnblogs_postid: "18486604"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18486604"
---

# 梦开始的地方
## 第一~二周
1.	misc-decompress
将所有压缩文件放在一个目录，使用Bandizip解压.001，然后使用md5计算器计算内部内容，即可获得flag

2.	misc-用溯流仪见证伏特台
首先进入所给链接找到威胁盟报告，发现由于b站原因导致视频不清晰，于是下载央视频后搜索该新闻，再读出信息powerj7kmpzkdhjg4szvcxxgktgk36ezpjxvtosylrpey7svpmrjyuyd.onion，最后计算md5获得flag
![image](/assets/cnblogs/2024 NewStarCTF-WP/3539156-20241019212956112-1495415680.png)

3.	crypto-base
使用base64解工具解码即可获得flag

4.	ez_answer
官方调查问卷

## 第三周
1. OSINT-MASTER
①首先看照片，机翼上有飞机注册号确定飞机编号（B-2419） 
![image](/assets/cnblogs/2024 NewStarCTF-WP/3539156-20241019213053442-171719515.png)

②随后确定拍摄时间（在属性里可以找到） 
![image](/assets/cnblogs/2024 NewStarCTF-WP/3539156-20241019213117825-1488648053.png)

③使用FlightAware 确定航班号MU5156 
④确定城市，使用flightADSB查看航班路径，再一个一个试（我尽力了
www） 
![image](/assets/cnblogs/2024 NewStarCTF-WP/3539156-20241019213137109-1671614843.png)

2. AmazingGame
打20关（？得到flag
![image](/assets/cnblogs/2024 NewStarCTF-WP/3539156-20241019213147317-921358017.png)

## 第四周
1. 圣石匕首 
使用SageMath Notebook 
通过计算得到flag
![image](/assets/cnblogs/2024 NewStarCTF-WP/3539156-20241021095432879-1686036664.png)
![image](/assets/cnblogs/2024 NewStarCTF-WP/3539156-20241021095447442-719732596.png)

2. 扫码领取flag 
解压后得到5个文件，首先用TrIDNET看各个文件，发现全为png格式，于是全改为png文件 
![image](/assets/cnblogs/2024 NewStarCTF-WP/3539156-20241021095512955-1305965253.png)

注意到压缩包名为CRC，考虑用crc 宽高进行爆破 
![image](/assets/cnblogs/2024 NewStarCTF-WP/3539156-20241021095526667-603914117.png)
![image](/assets/cnblogs/2024 NewStarCTF-WP/3539156-20241021095537944-1260610654.png)
最后四个图片可以拼出一个码，用扫码网站扫描即可获得flag
![image](/assets/cnblogs/2024 NewStarCTF-WP/3539156-20241021095548662-1199096841.png)

## 第五周
Ljnljn的WriteUP（4）
1.	reverse-lock
解压后得到一个.py和.pyd文件，运行python文件发现要输入密码，然后分析代码
发现提示Hint: The password is 20 characters long and only contains letters and numbers from 0 to f.，故尝试一下爆破
由于20!= 2432902008176640000过于庞大，首先试试用一个一个数字攻破的方法计算
![image](/assets/cnblogs/2024 NewStarCTF-WP/3539156-20241028074331599-733982841.png)
然后使用itertools.permutations（）进行全排列小范围爆破
![image](/assets/cnblogs/2024 NewStarCTF-WP/3539156-20241028074320116-593578962.png)
爆破后得出结果
![image](/assets/cnblogs/2024 NewStarCTF-WP/3539156-20241028074349938-1382302082.png)
password即为flag
