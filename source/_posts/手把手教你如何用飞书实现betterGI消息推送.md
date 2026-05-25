---
title: "手把手教你如何用飞书实现betterGI消息推送"
date: 2025-02-08 23:30:00
categories:
  - "Others"
tags:
cnblogs_postid: "18705592"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18705592"
---

在平时，我们一般会使用betterGI的一条龙系统来完成体力的刷取，有的人可能需要知道啥时候刷完体力方便远程关闭电脑啥的，这里给大家如何通过飞书实现BetterGI消息推送的方法
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
先新建一个群聊
![image](/assets/cnblogs/手把手教你如何用飞书实现betterGI消息推送/3539156-20250208232030493-2081467331.png)
![image](/assets/cnblogs/手把手教你如何用飞书实现betterGI消息推送/3539156-20250208232118432-685521840.png)
再选中设置
![image](/assets/cnblogs/手把手教你如何用飞书实现betterGI消息推送/3539156-20250208232209820-288477870.png)
选中群机器人
![image](/assets/cnblogs/手把手教你如何用飞书实现betterGI消息推送/3539156-20250208232237090-1998906819.png)
选中添加自定义机器人
![image](/assets/cnblogs/手把手教你如何用飞书实现betterGI消息推送/3539156-20250208232354047-792692016.png)
写好描述后点击添加
把这里的webhook链接复制好，调一些安全设置（我这里怕有问题就没设置，一定要防止链接泄漏）
![image](/assets/cnblogs/手把手教你如何用飞书实现betterGI消息推送/3539156-20250208232535981-1091452916.png)
随后打开bettergi，选中设置，打开飞书推送，粘贴进地址，测试一下
![image](/assets/cnblogs/手把手教你如何用飞书实现betterGI消息推送/3539156-20250208232730064-63152374.png)
看到测试信息就调试好啦
![image](/assets/cnblogs/手把手教你如何用飞书实现betterGI消息推送/3539156-20250208232752430-977137120.png)
测试了下还不错
![image](/assets/cnblogs/手把手教你如何用飞书实现betterGI消息推送/3539156-20250209000934065-366102497.png)
