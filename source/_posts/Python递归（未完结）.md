---
title: "Python递归（未完结）"
date: 2024-12-04 19:37:00
categories:
  - "Programming"
tags:
  - "Programming"
  - "Python"
cnblogs_postid: "18587035"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18587035"
---

## 两个特点：
1、调用自身
2、结束条件
![image](/assets/cnblogs/Python递归（未完结）/3539156-20241204193450398-1823105583.png)
为什么func3打印321而func4打印123的原因（看套娃图理解，大框为func，小框为print）（3从外到内，4从内到外）

## 示例：汉诺塔问题
一共n个盘子，把上面的n-1个盘子看成一个整体
1. 把n-1个盘子从A经过C移动到B
2. 把第n个盘子从A移动到C（移动一步的情况）
3. 把n-1个盘子从B经过A移动到C
```
#!/user/bin/env python3
# -*- coding: utf-8 -*-
def hanoi(n,a,b,c):
    if n>0:
        hanoi(n-1,a,c,b)
        print(f'{a}->{c}')
        hanoi(n-1,b,a,c)

hanoi(30,'a','b','c')
```
递推式：h(x)=2h(x-1)+1
