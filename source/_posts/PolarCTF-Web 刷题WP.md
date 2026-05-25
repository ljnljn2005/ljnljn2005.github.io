---
title: "PolarCTF-Web 刷题WP"
date: 2024-12-10 20:50:00
categories:
  - "CTF Web"
tags:
  - "CTF"
  - "Web"
  - "PolarCTF"
cnblogs_postid: "18598005"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18598005"
---

1、坦诚相见
比赛结束前最后十分钟想着抢个flag做的，但是怎么都没想出来，比赛结束之后有感而发写一下
方法1：绕过，用分号隔开每个指令，因为屏蔽了flag所以用*通配符绕过
cd ..;cd ..;cd ..;sudo cat fl*g
![image](/assets/cnblogs/PolarCTF-Web 刷题WP/3539156-20241210204917043-906225724.png)
方法2：ls
![image](/assets/cnblogs/PolarCTF-Web 刷题WP/3539156-20241210204923171-539183289.png)
cat no.php发现过滤内容
![image](/assets/cnblogs/PolarCTF-Web 刷题WP/3539156-20241210204929587-1294947331.png)
rm no.php删除文件
然后cd ..;cd ..;cd ..;sudo cat flag
![image](/assets/cnblogs/PolarCTF-Web 刷题WP/3539156-20241210204935949-2061200086.png)
反思：
1、linux指令可以用分号隔开而写在一行
2、要提权执行指令，不然大概率失败（sudo）

2、iphone
按按钮的时候用burpsuite改UA
![image](/assets/cnblogs/PolarCTF-Web 刷题WP/3539156-20241212210724148-176183024.png)
出现flag
![image](/assets/cnblogs/PolarCTF-Web 刷题WP/3539156-20241212210734016-1184576426.png)
