---
title: "Python输入多个变量和输入列表"
date: 2024-11-30 10:46:00
categories:
  - "Programming"
tags:
  - "Programming"
  - "Python"
cnblogs_postid: "18578160"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18578160"
---

## 输入多个变量:map
map()函数的基本用法是将一个函数和一个可迭代对象作为参数传递给它，然后返回一个迭代器，该迭代器会生成经过指定函数转换后的元素。
```
a,b=map(int,input().split())
```
例题：P1980 [NOIP2013 普及组] 计数问题
```
numlist = []
count = 0
n, x = map(int, input().split())
for i in range(1, n + 1):
    count = count + str(i).count(str(x))
print(count)
```
## 输入一整个列表：map或列表推导式
### map方法：
```
num=list(map(int, input().split()))
```
例题：P1059 [NOIP2006 普及组] 明明的随机数
```
#!/user/bin/env python3
# -*- coding: utf-8 -*-
n= int(input())
randomnum=list(map(int, input().split()))
randomnum2=[]
for i in range(n):
    suijishu=randomnum[i]
    if suijishu in randomnum2:
        continue
    else:
        randomnum2.append(suijishu)
print(len(randomnum2))
randomnum2.sort()
for i in range(len(randomnum2)):
    print(randomnum2[i],end=' ')
```
### 列表推导式方法：
```
a = [int(x) for x in input().split()]
```
例题：P1427 小鱼的数字游戏
```
#!/user/bin/env python3
# -*- coding: utf-8 -*-
ai = [int(x) for x in input().split()]
del ai[-1]
ai.reverse()
for i in ai:
    print(i, end=' ')
```
