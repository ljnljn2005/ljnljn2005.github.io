---
title: "每日一题：BUUCTF38-刷新过的图片"
date: 2025-01-02 11:27:00
categories:
  - "CTF Writeup"
tags:
  - "CTF"
  - "Writeup"
  - "BUUCTF"
  - "Misc"
cnblogs_postid: "18647271"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18647271"
---

用基础的分析图片没有什么内容
随后看提示提示：浏览图片的时候刷新键有没有用呢
刷新对应F5隐写，所以进行F5隐写试一下
注意F5隐写对应java8，用其他版本可能报错（被坑了）
![image](/assets/cnblogs/每日一题：BUUCTF38-刷新过的图片/3539156-20250102112222713-1062276770.png)
随后打开output.txt，用notepad打开是乱码，用010打开一眼zip
压缩包是伪加密，修复一下
得到flag
![image](/assets/cnblogs/每日一题：BUUCTF38-刷新过的图片/3539156-20250102112643724-641117895.png)
