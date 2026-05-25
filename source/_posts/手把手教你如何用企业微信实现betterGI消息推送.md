---
title: "手把手教你如何用企业微信实现betterGI消息推送"
date: 2025-02-08 23:42:00
categories:
  - "Others"
tags:
cnblogs_postid: "18705602"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18705602"
---

在平时，我们一般会使用betterGI的一条龙系统来完成体力的刷取，有的人可能需要知道啥时候刷完体力方便远程关闭电脑啥的，这里给大家如何通过企业微信实现BetterGI消息推送的方法
（我还写了一篇飞书的大家可以看看）
## 1、支持的事件提醒
事件列表
notify.test : 测试通知
domain.reward : 自动秘境奖励
domain.start : 自动秘境启动
domain.end : 自动秘境结束
domain.retry : 自动秘境重试
task.cancel : 任务启动
task.error : 任务错误
group.start : 配置组启动
group.end : 配置组结束
dragon.start : 一条龙启动
dragon.end : 一条龙结束
tcg.start : 七圣召唤启动
tcg.end : 七圣召唤结束
album.start : 自动音游专辑启动
album.end : 自动音游专辑结束
album.error : 自动音游专辑错误
## 2、创建方法
先新建一个群聊，这里需要拉两个人加上自己创建一个，然后再把另外两个人踢了就行
![image](/assets/cnblogs/手把手教你如何用企业微信实现betterGI消息推送/3539156-20250208233956930-1621704568.png)
再选中三个点，选中群机器人
![image](/assets/cnblogs/手把手教你如何用企业微信实现betterGI消息推送/3539156-20250208233931602-1833333795.png)
选中添加机器人——创建一个机器人
写好描述后点击添加
把这里的webhook链接复制好
![image](/assets/cnblogs/手把手教你如何用企业微信实现betterGI消息推送/3539156-20250208234058147-1588847764.png)
随后打开bettergi，选中设置，打开企业微信推送，粘贴进地址，测试一下
![image](/assets/cnblogs/手把手教你如何用企业微信实现betterGI消息推送/3539156-20250208234139057-1878211697.png)
看到测试信息就调试好啦
![image](/assets/cnblogs/手把手教你如何用企业微信实现betterGI消息推送/3539156-20250208234154867-1158900905.png)
