---
title: "使用服务器docker搭建Pwn题目"
date: 2024-12-02 19:13:00
categories:
  - "CTF Writeup"
tags:
  - "CTF"
  - "Writeup"
  - "Pwn"
  - "Linux"
cnblogs_postid: "18582505"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18582505"
---

# 一、docker的安装
## 1、安装前先卸载操作系统默认安装的docker
```sudo apt-get remove docker docker-engine docker.io containerd runc```
## 2、安装必要支持
```sudo apt install apt-transport-https ca-certificates curl software-properties-common gnupg lsb-release```
## 3、添加gpg KEY（阿里云）
```curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg```
## 4、添加apt源
```
#阿里apt源
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
## 5、更新源
```sudo apt update
sudo apt-get update
```
## 6、安装Docker
```
#安装最新版本的Docker
sudo apt install docker-ce docker-ce-cli containerd.io
#查看Docker版本
sudo docker version
#查看Docker运行状态
sudo systemctl status docker
```
## 7、安装docker-compose
```
sudo apt install docker-compose
```
## 8、下载github上的deploy_pwn_template环境
```
git clone https://github.com/RoderickChan/deploy_pwn_template
```
## 9、选择一个适合的环境（我选的pwn-unbutu_22.04）,先确保已经编译好了pwn的题目，将其放在src里面并改名为attachment（把以前那个删掉）
![image](/assets/cnblogs/使用服务器docker搭建Pwn题目/3539156-20241202190140056-849494603.png)
## 10、打开docker文件夹并打开docker-compose，更改一下端口
![image](/assets/cnblogs/使用服务器docker搭建Pwn题目/3539156-20241202190507853-2141222296.png)
（这是最简单的方法，如果有其他要求的话（比如多个docker实例）就按照markdown文档的修改）
补充：在docker-compose.yml下可以修改第二行test来增加多个实例
```
services:
  test:
    build: ../
    environment:
      # 仅为测试用flag
      FLAG: "flag{haha_shellcode}"
    ports:
      # 设置了暴露端口
      - 20005:9999
    restart: unless-stopped
```

## 11、构建docker实例
在docker文件夹输入
```
docker-compose up
```
搭建实例
![image](/assets/cnblogs/使用服务器docker搭建Pwn题目/3539156-20241202191018018-1251892467.png)
显示如下内容就是搭建好了
![image](/assets/cnblogs/使用服务器docker搭建Pwn题目/3539156-20241202190900852-411895485.png)
最后使用nc测试和pwntools都没有问题
![image](/assets/cnblogs/使用服务器docker搭建Pwn题目/3539156-20241202191109739-1981457607.png)
![image](/assets/cnblogs/使用服务器docker搭建Pwn题目/3539156-20241202191145369-607010858.png)
