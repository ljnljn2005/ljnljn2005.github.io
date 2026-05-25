---
title: "misc长宽高爆破"
date: 2024-10-16 19:41:00
categories:
  - "CTF Misc"
tags:
  - "CTF"
  - "Misc"
cnblogs_postid: "18470618"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18470618"
---

**png文件结构**
![](/assets/cnblogs/misc长宽高爆破/3539156-20241016201252120-753750872.png)
①：IHDR（文件头数据块）
包含存储图片数据的基本信息，一个png文件只能有一个IHDR
 ②：IDAT（图像数据块）
存放图片真正的数据信息（可以有多个，正常情况下必须把上一个填
满才能填下一个，不正常大概率就是有隐写了）
③：IEND（图像结束数据）
标记png文件或者数据流的结束，且放到文件的尾部
（根据这个可以判断一个图片里面是否会含有第二个隐藏图片，即是
否有隐写，到时候就需要用到分离图片工具进行下一步操作）

**使用Stegsolve**
![](/assets/cnblogs/misc长宽高爆破/3539156-20241016194023985-1848195136.png)
