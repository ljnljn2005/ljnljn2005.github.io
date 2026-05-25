---
title: "Yak学习3：基础语法3复合数据类型"
date: 2026-02-14 20:26:00
categories:
  - "Others"
tags:
cnblogs_postid: "19616547"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/19616547"
---

## 列表list
中括号
列表中有不同数据类型，列表类型为any
列表内只有整数，列表类型为int
列表又有整数又有浮点数，列表类型为float

可以用`make([]类型<,元素数量>)`创建列表
列表操作指令
```
a=[1,2]
b=[4,5,6]
a=append(a,3) a为`[1,2,3]`
a=a+b a为`[1,2,3,4,5,6]`
a[0] 输出1
a[:2] 输出[1,2]
a[::-1] 输出[6,5,4,3,2,1]
```
内置方法
```
a.Append(1)、a.Push(1) 在数组后追加元素1
a.Pop([index]) 弹出数组最后一个元素（不带index时）
a.Extend(b)、a.Merge(b) 用新数组扩展原数组
```
![assets/Yak学习3：基础语法3复合数据类型/file-20260214195106943.png](/assets/cnblogs/Yak学习3：基础语法3复合数据类型/3539156-20260214202600558-396435207.png)
```
a.Length()、a.Len() 获取数组长度
a.Capability、a.Cap() 获取数组容量
a.StringSlice() 将数组转换成[]string
a.GeneralSlice() 将数组转换成最泛化的类型[]any
a.Shift() 数组开头移除一个元素
a.Unshift() 数组开头增加一个元素
a.Map(func(i){return i*2})对数组每个元素进行指定函数运算后返回结果
a.Filter(func(i){return i>2})对数组每个元素进行指定函数过滤后返回结果
a.Insert(1,2)在指定位置插入元素
a.Remove(1)移除数组第一次出现的元素
a.Reverse()反转
a.Sort([reverse])排序（reverse是否反向）
a.Clear()清空
a.Count()计算元素数量
a.Index(i)返回第i-1个元素
```
## 字典map
### 创建字典
m={"a":1,"b":2} -> type: `map[string]int`
m1={1:2,"3":"4","5":6.0} -> type:`map[interface{}]interface{}`
```
a=make(map[string]int<,2>)后面可选指定容量
a["a"]=1
println(a) -> map[a:1]
```
### 基本操作
基本操作和列表类似
获取字典中不存在的值会返回undefined
获取长度len(a)
获取值`a["e"]、a.f`
特殊的：a.$v用于在字典a中查找键为v的值
例如
v="b"
a={"b":"hihihi"}
println(a.$v) -> hihihi
### 添加、删除值
```
a["e"]=1
a.f=2
```
删除delete(a,"b")
### 方法
a.Keys() 获取所有元素的键key
a.Values() 获取所有元素的Value值
a.Entries() / a.Items() 获取所有元素的Entity
![assets/Yak学习3：基础语法3复合数据类型/file-20260214201322072.png](/assets/cnblogs/Yak学习3：基础语法3复合数据类型/3539156-20260214202600479-648420719.png)
a.Foreach(func(k,v){println(k,v)})  遍历元素
a.Set("key","value") 设置元素的值，若key不存在则添加
a.Remove("key") / a.Delete("key") 删除一个值
a.Has("key") / a.IsExisted("key") 判断是否包含key
a.Length() / a.Len() 长度
## 通道channel
创建
ch:=make(chan int)
ch2:=make(chan var,2)这里设定了存储空间为2个
写入
ch<-1 没写存储空间会阻塞
读取
v:=<-ch
检查是否取走包裹成功
v,ok:=<-ch
if ok{println("success")}
![assets/Yak学习3：基础语法3复合数据类型/file-20260214202317782.png](/assets/cnblogs/Yak学习3：基础语法3复合数据类型/3539156-20260214202600497-1597655866.png)
len(ch) 查看还有多少个包裹
cap(ch) 查看最多存放多少个包裹
close(ch) 关闭channel
for v=range ch2{println(v)} 遍历取走所有包裹
