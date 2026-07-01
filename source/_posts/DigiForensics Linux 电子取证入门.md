---
title: "DigiForensics Linux 电子取证入门"
date: 2026-06-05 17:55
categories:
  - "Forensics Notes"
tags:
  - "Forensics"
  - "DigiForensics"
  - "Linux"
cnblogs_postid: "20332676"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/20332676"
---

<h2>检材中新增的本地普通用户有哪些？</h2>
<p>直接看用户列表即可<br/>
<img alt="assets/DigiForensics Linux 电子取证入门/file-20260605173445876.png" src="https://img2024.cnblogs.com/blog/3539156/202606/3539156-20260605175514472-1621375671.png"/></p>
<h2><code>ops</code> 用户家目录中用于记录值班信息的文本文件名是什么？</h2>
<p><img alt="assets/DigiForensics Linux 电子取证入门/file-20260605173812405.png" src="https://img2024.cnblogs.com/blog/3539156/202606/3539156-20260605175514720-299716575.png"/></p>
<h2>在新增普通用户中，哪个用户未发现明显交互登录痕迹？</h2>
<p>第一题有三个用户作为答案，接下来看命令执行，这里看出backup是有操作的<br/>
<img alt="assets/DigiForensics Linux 电子取证入门/file-20260605173954501.png" src="https://img2024.cnblogs.com/blog/3539156/202606/3539156-20260605175514527-1140654613.png"/><br/>
上一题ops是有home目录的，说明也进行了操作<br/>
那就说明tempuser没有实际操作</p>
<h2>SSH 服务的主配置文件路径是什么？</h2>
<p>知识哦<br/>
<img alt="assets/DigiForensics Linux 电子取证入门/file-20260605174222383.png" src="https://img2024.cnblogs.com/blog/3539156/202606/3539156-20260605175514713-1116259883.png"/></p>
<h2>从服务状态、配置文件和日志综合判断，检材中重点启用过哪些网络服务？</h2>
<p>就看到这俩<br/>
<img alt="assets/DigiForensics Linux 电子取证入门/file-20260605174431733.png" src="https://img2024.cnblogs.com/blog/3539156/202606/3539156-20260605175514758-1230059696.png"/></p>
<h2>SSH 服务存在开机自启动配置痕迹。</h2>
<p><img alt="assets/DigiForensics Linux 电子取证入门/file-20260605174400371.png" src="https://img2024.cnblogs.com/blog/3539156/202606/3539156-20260605175514624-2109553146.png"/></p>
<h2>业务首页正文中记录的管理员账号是什么？</h2>
<p>网站目录如果没有面板一般在/var/www/html<br/>
<img alt="assets/DigiForensics Linux 电子取证入门/file-20260605174535443.png" src="https://img2024.cnblogs.com/blog/3539156/202606/3539156-20260605175514589-668360708.png"/></p>
<h2>Nginx 访问日志中可见哪些请求路径？</h2>
<p>先找到日志在/var/log/nginx<br/>
<img alt="assets/DigiForensics Linux 电子取证入门/file-20260605174611996.png" src="https://img2024.cnblogs.com/blog/3539156/202606/3539156-20260605175514493-53623017.png"/><br/>
<img alt="assets/DigiForensics Linux 电子取证入门/file-20260605174631780.png" src="https://img2024.cnblogs.com/blog/3539156/202606/3539156-20260605175514274-290667391.png"/></p>
<h2><code>/test404</code> 请求对应的 HTTP 状态码是什么？</h2>
<p>见上题</p>
<h2>访问日志中存在对 <code>/portal/readme.txt</code> 的成功访问记录。</h2>
<p>见上上题<br/>
注意这里返回的是200而且是有大小的，说明访问成功了</p>
<h2><code>/srv/uploads</code> 目录下的核心文件包括哪些？</h2>
<p><img alt="assets/DigiForensics Linux 电子取证入门/file-20260605174838965.png" src="https://img2024.cnblogs.com/blog/3539156/202606/3539156-20260605175514603-709271193.png"/><br/>
第四个其实在定时任务可以看到但不在这个文件夹，这里不赘述</p>
<h2><code>/srv/uploads/notice.txt</code> 中记录的签到码是多少？</h2>
<p><img alt="assets/DigiForensics Linux 电子取证入门/file-20260605174913381.png" src="https://img2024.cnblogs.com/blog/3539156/202606/3539156-20260605175514610-1245525915.png"/></p>
<h2>结合命令历史，读取 <code>account.txt</code> 前所在的工作目录是什么？</h2>
<p>先找到这个命令在dfadmin<br/>
<img alt="assets/DigiForensics Linux 电子取证入门/file-20260605175002434.png" src="https://img2024.cnblogs.com/blog/3539156/202606/3539156-20260605175514535-439779183.png"/><br/>
再翻一下就可以看到cd指令指向的目录<br/>
<img alt="assets/DigiForensics Linux 电子取证入门/file-20260605175508416.png" src="https://img2024.cnblogs.com/blog/3539156/202606/3539156-20260605175514653-1927069757.png"/></p>
<h2>root 计划任务调用的脚本路径是什么？</h2>
<p><img alt="assets/DigiForensics Linux 电子取证入门/file-20260605175247342.png" src="https://img2024.cnblogs.com/blog/3539156/202606/3539156-20260605175514690-677979867.png"/></p>
<h2>root 计划任务的执行时间是什么？</h2>
<p>见上题</p>
<h2>SSH 配置修改发生在 SSH 服务重启之前。</h2>
<p><img alt="assets/DigiForensics Linux 电子取证入门/file-20260605175440887.png" src="https://img2024.cnblogs.com/blog/3539156/202606/3539156-20260605175514731-1615789202.png"/></p>
