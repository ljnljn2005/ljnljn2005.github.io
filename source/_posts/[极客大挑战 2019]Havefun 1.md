---
title: "[极客大挑战 2019]Havefun 1"
date: 2025-03-09 23:06:00
categories:
  - "Others"
tags:
cnblogs_postid: "18761606"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18761606"
---

进网站显示一只猫，于是看源代码
发现下面有注释
```
                <!--
        $cat=$_GET['cat'];
        echo $cat;
        if($cat=='dog'){
            echo 'Syc{cat_cat_cat_cat}';
        }
        -->
```
所以在后面加上```/index.php?cat=dog```即可（小猫可爱捏）
![image](/assets/cnblogs/[极客大挑战 2019]Havefun 1/3539156-20250309230559357-1393519121.png)
