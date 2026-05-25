---
title: "弱密码与BurpSuite爆破"
date: 2025-01-02 22:49:00
categories:
  - "CTF Web"
tags:
  - "CTF"
  - "Web"
  - "Crypto"
cnblogs_postid: "18648878"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18648878"
---

## 1、弱口令

![image](/assets/cnblogs/弱密码与BurpSuite爆破/3539156-20250102224734829-667527262.png)

![image](/assets/cnblogs/弱密码与BurpSuite爆破/3539156-20250102224739912-1625004001.png)

## 2、弱口令的分类

![image](/assets/cnblogs/弱密码与BurpSuite爆破/3539156-20250102224746803-108852233.png)

常见的数据库密码：

- root
- root123、123456
- tomcat
- jboss

![image](/assets/cnblogs/弱密码与BurpSuite爆破/3539156-20250102224752520-897615099.png)

## 3、暴力破解

### 用暴力方式进行破解

#### 后台系统登录界面

- 爆破
- SQL注入 万能密码
- xss
- 未授权访问
- 扫子域名
- js文件

## 4、Burpsuite的使用和用bp爆破密码

### 设置https代理插件

![image](/assets/cnblogs/弱密码与BurpSuite爆破/3539156-20250102224803010-22310025.png)

导入证书

![image](/assets/cnblogs/弱密码与BurpSuite爆破/3539156-20250102224807524-1225670284.png)

![image](/assets/cnblogs/弱密码与BurpSuite爆破/3539156-20250102224812827-392584306.png)

![image](/assets/cnblogs/弱密码与BurpSuite爆破/3539156-20250102224818318-1338068323.png)

成功

![image](/assets/cnblogs/弱密码与BurpSuite爆破/3539156-20250102224822892-823871670.png)

### bp的作用

![image](/assets/cnblogs/弱密码与BurpSuite爆破/3539156-20250102224828003-234101045.png)

burp能篡改内容

示例：

![image](/assets/cnblogs/弱密码与BurpSuite爆破/3539156-20250102224833468-1823868064.png)

点Render可以显示网页

![image](/assets/cnblogs/弱密码与BurpSuite爆破/3539156-20250102224837640-98822480.png)

### 用bp爆破密码

#### 1、狙击手模式

添加payload位置

![image](/assets/cnblogs/弱密码与BurpSuite爆破/3539156-20250102224842437-378749704.png)

创建字典

![image](/assets/cnblogs/弱密码与BurpSuite爆破/3539156-20250102224846912-249858242.png)

发现长度不一致，筛选出可能正确的密码

![image](/assets/cnblogs/弱密码与BurpSuite爆破/3539156-20250102224851602-1782752289.png)

渲染网页发现正确

![image](/assets/cnblogs/弱密码与BurpSuite爆破/3539156-20250102224855955-970897349.png)

#### 2、battering ram模式

把所有的标记位置用相同的字典内容替换（后面多的会被舍弃，一个对应一个)

#### 3、pitchfork模式

两个字典一一对应

![image](/assets/cnblogs/弱密码与BurpSuite爆破/3539156-20250102224902149-880236486.png)

#### 4、Cluster Bomb模式（更全面）（更好用）（时间更久）

直接两个字典全排列爆破

![image](/assets/cnblogs/弱密码与BurpSuite爆破/3539156-20250102224906823-523770189.png)

加解密的处理：bp自带加解密

![image](/assets/cnblogs/弱密码与BurpSuite爆破/3539156-20250102224911994-1286324415.png)

## 5、如何防御

从开发者角度：

①密码密文传输

②限制错误次数

③二次验证（图片验证、短信验证、二维码、人脸识别、滑块验......）

④锁定ip，禁止访问0

从用户角度：

①密码尽量复杂

②不同网站用不同密码（防止撞库） 

③定期修改密码

④上网时检查域名，防止被钓鱼

## 6、在线加密网站

![image](/assets/cnblogs/弱密码与BurpSuite爆破/3539156-20250102224916957-1322230793.png)
