---
title: "“setprecision”: 找不到标识符/“operator <<”不明确的解决方案"
date: 2024-10-20 20:14:00
categories:
  - "Programming"
tags:
  - "Programming"
  - "C++"
cnblogs_postid: "18487787"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18487787"
---

> 题目：P5706 【深基2.例8】再分肥宅水

使用vs2022编程时使用cout格式化出现如下错误
![](/assets/cnblogs/“setprecision”- 找不到标识符-“operator --”不明确的解决方案/3539156-20241020201205054-69161242.png)
经查阅，是因为iomanip头文件未加载，只需在文件头加上
```
#include<iomanip>
```
即可

添加后正常运行
![](/assets/cnblogs/“setprecision”- 找不到标识符-“operator --”不明确的解决方案/3539156-20241020201501927-1050184082.png)
