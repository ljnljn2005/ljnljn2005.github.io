---
title: "Python算法学习1-Python基础"
date: 2024-10-28 08:19:00
categories:
  - "Programming"
tags:
  - "Programming"
  - "Python"
cnblogs_postid: "18509539"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18509539"
---

1. 写在一行上的多行语句用分号分割
```
a=input();a=int(a)
print(a+1)
```
2. Python IDLE快捷键
按Alt+3注释选中的多行代码，Alt+4取消
Ctrl+[向左减少缩进，Ctrl+]向右增加缩进
3. input.split()将字符串以指定方法分割（默认为空格）
```
a,b=input().split#第一种用法
a=input().split#第二种用法，输出为列表
```
4. 反斜杠‘\’为续行符，可以让一行语句分行
```
a\
=\
1
print(a)
```
5. print格式化
%d-整型，%f-浮点型，%s-字符串型
```
print("%d"%(1+2))#输出3
print("%d+%d=%d"%(1,2,1+2))#输出1+2=3
print("%.2f"%3.14159)#输出3.14(.2f保留两位小数)
t="hello"
print("%s"%t)#输出hello
print("%c"%'A')#输出A
print("%c"%65)#输出A
```
注意有多个时用小括号括起来，中间用逗号隔开
另外还有一种方法显示变量值
```
print(f"name is {name}")
print(f"number is {number:.2f}")
```
6. ASCII码和字符的转换
ord()字符转为ASCII码
chr()ASCII码转为字符
