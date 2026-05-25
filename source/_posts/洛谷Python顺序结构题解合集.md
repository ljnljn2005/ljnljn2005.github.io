---
title: "洛谷Python顺序结构题解合集"
date: 2024-10-31 20:21:00
categories:
  - "Programming"
tags:
  - "Programming"
  - "Python"
cnblogs_postid: "18518792"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18518792"
---

### P5705【深基2.例7】数字反转
```s=str(input())
a=s[0]
b=s[1]
c=s[2]
d=s[4]
print(f"{d}.{c}{b}{a}")
```
### P5706【深基2.例8】再分肥宅水	
```a=input().split()
ans=float(a[0])/int(a[1])
beizi=2*int(a[1])
print(f"{ans:.3f}\n{beizi}")
```
### P5708【深基2.习2】三角形面积
```a,b,c=map(float,input().split())
p=0.5*(a+b+c)
ans=pow((p*(p-a)*(p-b)*(p-c)),0.5)
print(f"{ans:.1f}")
```
### B2029 大象喝水
```#!/user/bin/env python3
# -*- coding: utf-8 -*-
h,r= map(int,input().split())
v=3.14*r*r*h
tong=int(20000//v)
print(tong+1)```
