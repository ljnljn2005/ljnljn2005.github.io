---
title: "wsl kali运行docker踩坑"
date: 2025-05-20 19:13:00
categories:
  - "Security Notes"
tags:
  - "Security"
  - "Linux"
cnblogs_postid: "18887640"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18887640"
---

# 1.docker服务没有启动
![image](/assets/cnblogs/wsl kali运行docker踩坑/3539156-20250520191026058-221782753.png)
启动docker失败了，然后想用systemctl启动但是还是失败
尝试安装也失败
![image](/assets/cnblogs/wsl kali运行docker踩坑/3539156-20250520191111705-1040412876.png)
后面搜索后尝试用service docker start替换，成功
![image](/assets/cnblogs/wsl kali运行docker踩坑/3539156-20250520191141624-1322569246.png)
# 2.镜像无法pull
网络问题，看这个
https://cloud.tencent.com/developer/article/2485043
更换镜像源之后成功
![image](/assets/cnblogs/wsl kali运行docker踩坑/3539156-20250520191244385-1986941564.png)
