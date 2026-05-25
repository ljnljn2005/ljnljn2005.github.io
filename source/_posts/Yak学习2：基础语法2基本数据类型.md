---
title: "Yak学习2：基础语法2基本数据类型"
date: 2026-02-13 19:50:00
categories:
  - "Others"
tags:
cnblogs_postid: "19613413"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/19613413"
---

int 带正负号的整数数据类型
string 字符数据类型
float 浮点数
byte 无符号8位整数，表示一个字节（二进制字符串：`[]byte`）
nil、undefined 未定义的变量或者空值
bool 布尔值（true、false）
### 整数和浮点数
#### 各种进制的申明
二进制 
a=0b10
println(a) -> 2
八进制
b=0100
println(b) -> 64
十六进制
d=0x10
println(d) ->16
#### 转换
整数和浮点数一起运算时，整数会先转换成浮点数再进行运算
### 空值
a=nil
a == undefined
a == nil
上面两个判断语句都返回true
### 字符申明
c='c'
println(c) -> 99
本质上单个字符的底层类型是uint8
### 字符串
经典字符串：双引号
文本块（多行字符串）：反引号"\`"
字节序列：双引号前加b
![assets/Yak学习2：基础语法2基本数据类型/file-20260213105914920.png](/assets/cnblogs/Yak学习2：基础语法2基本数据类型/3539156-20260213195022034-2088272629.png)
#### 字符串格式化
常用于printf、println
%v 根据变量类型自动选择格式
%T 输出变量的类型
%d 十进制整数
%b 八进制整数
%x 小写十六进制
%X 大写十六进制
%f 浮点数，不带指数部分
%c ascii码对应的字符
%q 带引号的字符或者字符串
![assets/Yak学习2：基础语法2基本数据类型/file-20260213113348216.png](/assets/cnblogs/Yak学习2：基础语法2基本数据类型/3539156-20260213195022151-1860231370.png)
%s 字符串
%p 十六进制表示的内存地址或引用
#### 和python类似的f-string
双引号前加f，变量外加${}，直接输出变量
![assets/Yak学习2：基础语法2基本数据类型/file-20260213113629527.png](/assets/cnblogs/Yak学习2：基础语法2基本数据类型/3539156-20260213195022192-160573142.png)
#### 新增x-string
感觉像是模板，后面会有详细讲解
![assets/Yak学习2：基础语法2基本数据类型/file-20260213113927723.png](/assets/cnblogs/Yak学习2：基础语法2基本数据类型/3539156-20260213195022081-469292752.png)
#### 字符串运算
+进行字符串连接
\* 进行字符串的乘（和python类似）
\[:] 进行字符串切片（python类似）
#### 字符串方法
.First() 获取字符串第一个字符
.Reverse() 将字符串倒置
.Shuffle() 随机打乱字符串
.Fuzz({"params":"value"}) 对字符串进行模糊处理
.Contains("abc") 判断字符串是否包含后面的字符
.IContains("abc") 判断字符串是否包含后面的字符（忽略大小写）
.ReplaceN("abc","123",1) -> abcabc:123abc
.ReplaceAll("abc","123")  -> abcabc:123123
.Split(" ") 分割字符串
`.Join(["1","2"])`连接字符串
.Trim(" ") 去除字符串两端的cutset
.TrimLeft(" ")去除左侧的
.TrimRight(" ")去除右侧的
![assets/Yak学习2：基础语法2基本数据类型/file-20260213153652695.png](/assets/cnblogs/Yak学习2：基础语法2基本数据类型/3539156-20260213195022102-1474290915.png)
.HasPrefix("abc") 判断字符串是否以abc开头
.RemovePrefix("abc") 移除前缀
.HasSuffix("abc") 判断字符串是否以abc结尾
.RemoveSuffix("abc") 移除后缀
.Zfill(5) 字符串左侧填充0到5位（42->00042）
.RZfill(5) 字符串右侧填充0到5位
.Ljust(5) 左对齐，右侧填充空格到5位
.Rjust(5) 右对齐，左侧填充空格到5位
.Count("a") 统计a出现对的次数
.Find("a") 查找a第一次出现的位置
.RFind("a") 查找a最后一次出现的位置
.Lower() 字符串转小写
.Upper() 字符串转大写
.Title() 字符串转Title格式
.IsLower() 判断字符串是否为小写
.IsUpper() 判断字符串是否为大写
.IsTitle() 判断字符串是否为Title格式
.IsAlpha() 判断字符串是否为字母
.IsDigit() 判断字符串是否为数字
.IsAlnum() 判断字符串是否为字母或数字
.IsPrintable() 判断字符串是否为可打印字符
