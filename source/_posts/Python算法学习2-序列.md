---
title: "Python算法学习2-序列"
date: 2024-10-28 08:40:00
categories:
  - "Programming"
tags:
  - "Programming"
  - "Python"
cnblogs_postid: "18509554"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18509554"
---

序列名[下标]或序列名[-序号]引用序列中各个元素
```
s="abcdefg"
s[0]#'a'
s[6]#'g'
s[-1]#'g'
s[-7]#'a'
s[-4]#'d'
```
1. 列表
len()可以求列表中元素个数
list()可将迭代类型转化成列表
```
s='abcdefg'
s=list(s)
#s=['a','b','c','d','e','f','g']
```
2. 元组（tuple）
只包含一个元素后面要加逗号，如(1,)
同理（1,3,5）可以用t[0],t[1]等引用
tuple()可以将内容转换为元组
3. 字符串
常量，不可更改值
4. 切片
序列名[start:stop(:step)]
l[0:3]——提取l[0]~l[2]
l[len(l)//2]——提取后半部分（l[2]-l[4]）
l[:-1]截取除倒数第一个之外的字符
l[-4:-1]截取倒数第五个到倒数第一个之前的字符
