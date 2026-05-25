---
title: "PolarCTF-Misc 刷题WP"
date: 2024-12-06 17:11:00
categories:
  - "CTF Misc"
tags:
  - "CTF"
  - "Misc"
  - "PolarCTF"
cnblogs_postid: "18591163"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18591163"
---

随缘更新~
1、0和255
附件是python代码和输出内容
发现是图片转RGB值，于是转逆向的代码获得flag.png
```
# -*- coding = utf-8 -*-
# @software:PyCharm
from PIL import Image

image_list = ...

# 获取图像的宽高信息（假设宽高和之前打开的原始图像一致，这里示例写死，实际可以从image_list相关信息推断或者事先记录好）
width = len(image_list[0])
height = len(image_list)

# 创建一个新的图像对象
new_image = Image.new('RGB', (width, height))

# 将像素数据逐个设置到新图像中
for x in range(height):
    for y in range(width):
        new_image.putpixel((y, x), image_list[x][y])

# 保存图像为flag.png（如果需要保存为其他文件名或者格式，可以修改此处的文件名和格式后缀等）
new_image.save('flag.png')
```
得到二维码，解出flag
![image](/assets/cnblogs/PolarCTF-Misc 刷题WP/3539156-20241206171022959-1619632640.png)
