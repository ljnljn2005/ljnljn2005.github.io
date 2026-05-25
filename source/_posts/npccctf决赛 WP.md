---
title: "npccctf决赛 WP"
date: 2025-04-14 07:04:00
categories:
  - "CTF Writeup"
tags:
  - "CTF"
  - "Writeup"
  - "NPCCCTF"
cnblogs_postid: "18824099"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18824099"
---

# Misc

## 1、情书

上古牛帖

```
****-/*----/----*/****-/****-/*----/---**/*----/****-/*----/-****/***--/****-/*----/----*/**---/-****/**---/**---/***--/--***/****-/
女神说就五层
```

结合题目的提示以及之前的了解找到这个帖子的位置

https://tieba.baidu.com/p/529691897?pn=7

![image](/assets/cnblogs/npccctf决赛 WP/3539156-20250414070337085-2093370948.png)


试了一下，用veracrypt挂载，密码是iloveyoutoo

打开之后只有一个whereisflag，chkdsk发现有隐藏文件

![image](/assets/cnblogs/npccctf决赛 WP/3539156-20250414070341143-794514892.png)


用diskgenius打开可以提取出来

![image](/assets/cnblogs/npccctf决赛 WP/3539156-20250414070345200-1991950393.png)


然后打开rcrf这个文件，里面写着

```
ulpb vfde hfyz yisi buuima
key jqui xxmm vedrhx de qrpb xnxp
ulpb ui veyh dazide
```

搜索发现是小鹤双拼，把输入法改成这个就可以获得

![image](/assets/cnblogs/npccctf决赛 WP/3539156-20250414070350252-2130312006.png)


双拼 真的 很有 意思 不是吗 key 就是 下面 这段话 的 全品 小写 双拼 是 这样 打字的 shuangpinshizheyangdazide flag{shuangpinshizheyangdazide}

（其实发现了一道原题？）https://www.cnblogs.com/wgf4242/p/18622084

## 2、**final_happy**

密码在exif的base64字符串里（i_love_rose)

把所有隐写都试了一遍，最后发现是steghide
![image](/assets/cnblogs/npccctf决赛 WP/3539156-20250414070356174-695552196.png)


打开发现是16进制，并且发现是wav格式，但是直接打开又打不开，因此尝试修改文件头

![image](/assets/cnblogs/npccctf决赛 WP/3539156-20250414070400296-1029623715.png)


https://www.cnblogs.com/zhangxingcomeon/p/12613439.html

修改前后对比

![image](/assets/cnblogs/npccctf决赛 WP/3539156-20250414070404962-1871006401.png)


随后打开音频，明显是摩斯密码

注意这里结果要改小写中间用下划线隔开（这真不知道

flag{m4g1c_byt3s_1s_the_w4y}

# Web

## 1、**签个到吧**

```
?test=O:1:"A":2:{s:1:"a";N;s:1:"b";R:2;}
```
![image](/assets/cnblogs/npccctf决赛 WP/3539156-20250414070412823-1444321119.png)
