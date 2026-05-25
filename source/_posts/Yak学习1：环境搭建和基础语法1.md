---
title: "Yak学习1：环境搭建和基础语法1"
date: 2026-02-12 23:29:00
categories:
  - "Others"
tags:
cnblogs_postid: "19610084"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/19610084"
---

> 感谢知攻善防实验室抽奖赠送的《CDSL-YAK从入门到实践》，既然拿到了就好好学习一下

## 环境搭建
vscode里下yak语言插件
![assets/Yak学习1：环境搭建和基础语法1/file-20260212211653535.png](/assets/cnblogs/Yak学习1：环境搭建和基础语法1/3539156-20260212232927166-1522510080.png)
然后下载二进制文件
![assets/Yak学习1：环境搭建和基础语法1/file-20260212211905581.png](/assets/cnblogs/Yak学习1：环境搭建和基础语法1/3539156-20260212232927323-2102982593.png)
但是不知道为什么我这里是404
官方给了个安装命令（cmd打开）：`powershell (new-object System.Net.WebClient).DownloadFile('https://oss-qn.yaklang.com/yak/latest/yak_windows_amd64.exe','yak_windows_amd64.exe') && yak_windows_amd64.exe install && del /f yak_windows_amd64.exe`
输入后系统会自动安装
![assets/Yak学习1：环境搭建和基础语法1/file-20260212212058101.png](/assets/cnblogs/Yak学习1：环境搭建和基础语法1/3539156-20260212232927390-244330505.png)
这样就安装成功了
后面看好像yak这个插件只支持linux调试，所以用yakit继续学习
![assets/Yak学习1：环境搭建和基础语法1/file-20260212213057185.png](/assets/cnblogs/Yak学习1：环境搭建和基础语法1/3539156-20260212232927211-1338783005.png)
这个就可以启动yak编辑器
## 基础语法1
### 1、注释
`# 注释`
`// 注释`
`/* 这是多行注释 */`
### 2、变量申明
golang风格 var abc=123
强制创建 abc := 123
自动创建 abc=123
### 3、代码块
新的定义域
a=1;{a++;a+=12}
### 4、if控制流
有if/elif/else、if/else
if a>1{println("111")}
### 5、switch控制流
switch a{case 1,2,3:println("111")}
与break、fallstrough配套
### 6、循环
for in
`for a in [1,2,3]{println(a)}`
for range
`for _,a=range[1,2,3]{println(a)}`
for
`for i=1;i<10;i++{println(a)}`
`for{println("无限循环")}`
### 7、defer延迟执行语句
defer func{if recover()!=nil{println("catched")&#125;&#125;
### 8、go并发语句
go server.Start()
### 9、assert断言语句
`assert 1+1==2,"计算失败"`

后面会有详细说明
