---
title: "在Windows配置WSL2+VSCode编程环境"
date: 2024-11-28 21:13:00
categories:
  - "CTF Writeup"
tags:
  - "CTF"
  - "Writeup"
  - "Pwn"
  - "Python"
  - "C++"
  - "Linux"
cnblogs_postid: "18575203"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18575203"
---

> 感觉周围的人都是用的虚拟机运行linux+vscode，今天我想到一个更好的方法，用wsl2+vscode混合，可以在windows本地编代码，然后在linux内编译运行，非常的高效
配置教程：
## 1、开始菜单里搜索功能，并打开启用或关闭Windows功能
![image](/assets/cnblogs/在Windows配置WSL2+VSCode编程环境/3539156-20241128205131792-271071007.png)
打开框出的三个功能
![image](/assets/cnblogs/在Windows配置WSL2+VSCode编程环境/3539156-20241128205307516-471488090.png)
然后重启
## 2、在微软应用商店搜索kali linux（或者任何一个linux版本）安装
![image](/assets/cnblogs/在Windows配置WSL2+VSCode编程环境/3539156-20241128205409636-1821053961.png)
## 3、安装完成后，在kali linux下输入如下命令，安装工具集
```
sudo apt update && sudo apt upgrade
sudo apt install -y kali-linux-default
```
![image](/assets/cnblogs/在Windows配置WSL2+VSCode编程环境/3539156-20241128205859939-846309350.png)
（如果想要GUI的话可以安装win-kex，大佬链接：https://zhuanlan.zhihu.com/p/263658960）
## 4、vscode连接wsl
拓展里搜索wsl
![image](/assets/cnblogs/在Windows配置WSL2+VSCode编程环境/3539156-20241128210157368-1272692643.png)
按ctrl+shift+p打开命令界面，输wsl，选择WSL:Connect to WSL
![image](/assets/cnblogs/在Windows配置WSL2+VSCode编程环境/3539156-20241128210233443-381004426.png)
## 5、vscode拓展的安装
由于wsl连接的vscode拓展安装在wsl内，所以要重新安装拓展
![image](/assets/cnblogs/在Windows配置WSL2+VSCode编程环境/3539156-20241128210331706-186385543.png)
点击“在WSL：”这个按钮安装
## 6、vscode（wsl）的基本使用
### C++的运行
直接运行debugger就行
![image](/assets/cnblogs/在Windows配置WSL2+VSCode编程环境/3539156-20241128210939804-957250761.png)
没有的话先在终端运行
```
apt install gcc
```
### Python的运行
可以这样（右键-Run Python-Run Python in Terminal）
![image](/assets/cnblogs/在Windows配置WSL2+VSCode编程环境/3539156-20241128210452478-1296359373.png)
如果想要用Python Debugger运行的话看这个教程：https://blog.csdn.net/weixin_49895216/article/details/131696960
