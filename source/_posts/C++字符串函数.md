---
title: "C++字符串函数"
date: 2024-12-01 16:24:00
categories:
  - "CTF Writeup"
tags:
  - "CTF"
  - "Writeup"
  - "Pwn"
  - "C++"
cnblogs_postid: "18579896"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18579896"
---

## 两种字符串定义（C++）：
||字符串变量   | 字符数组   |
| ------------ | ------------ | ------------ |
|定义| string str;  | char str[100];  |
|求长度|str.length();/str.size();|strlen(str);|
|输入字符串|getline(cin,str);可以读入一行字符串，可以包含空格，遇到回车结束/cin>>str;可以读入一连串的字符，遇到空格or回车结束/scanf("%s",&str);遇到空格结束|cin.getline(str,sizeof(str));需要提前固定好输入的字符串的长度，避免输入的字符超出界限|
|分割截取|str.substr(7,3); // 从下标7开始截取子字符串，截取长度为3的字符串||
|查找指定子字符串|place=str.find("hi");||
|替换字符串中的一部分|str.replace(7, 5, "helloa");替换从下标7开始的5个字符为"helloa"||
|在指定位置插入字符串|str.insert(5, "try");||
|复制字符串|string str3(str1)/str3=str1;|str3 = str1;|
|排序|需要头文件#include \<algorithm>  sort(s.begin(), s.end());||
|删除|s.erase(s.begin()+2);使下标2的字符删掉||
|在字符串中添加字符|s.push_back('a');||

## C语言：
\#include\<cstring>
（1）复制字符串:strcpy(s1,s2);//复制s2到s1中
（2）连接字符串:strcat(s1,s2);连接字符串 s2 到字符串 s1 的末尾。
string str = str1 + str2;连接字符串也可以用+号
（3）返回字符串长度strlen(s1);
（4）比较字符串:strcmp(s1, s2);
如果 s1 和 s2 是相同的，则返回 0；如果 s1<s2 则返回值小于 0；如果 s1>s2 则返回值大于 0。
（5）查找字符strchr(s1, ch);返回一个指针，指向字符串 s1 中字符 ch 的第一次出现的位置。
