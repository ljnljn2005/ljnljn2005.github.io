---
title: "BurpSuite功能介绍"
date: 2024-11-18 18:37:00
categories:
  - "CTF Web"
tags:
  - "CTF"
  - "Web"
cnblogs_postid: "18553372"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18553372"
---

![](/assets/cnblogs/BurpSuite功能介绍/3539156-20241118183633269-973637187.png)

Burp Suite一共包含13个功能模块，它们帮助渗透测试人员更好地了解目标应用的整体状况、当前的工作涉及哪些目标、攻击面等信息。

Burp Suite Target主要包含站点地图、目标域、Target工具域并分析可能存在的漏洞。

Burp Suite Spider主要用于大型的应用系统测试，它能在很短时间内帮助我们快速了解系统的结构和分布情况。

Burp Suite Scanner主要用来自动检测Web系统的各种漏洞，可代替我们手动进行普通漏洞类型的渗透测试，从而使我们把更多精力放在那些必须人工验证的漏洞上。

Burp Suite Intruder在原始请求数据的基础上，通过修改各种请求参数获取不同的请求应答。在每一次请求中，Intruder通常会携带一个或多个有效攻击载荷，在不同的位置进行攻击重放，通过应答数据的比对分析获得需要的特征数据。

Burp Suite Repeater作为Burp Suite中一款手动验证HTTP消息的测试工具，通常用来抓取HTTP请求数据，并可重复对该请求数据做不同修改，以获取不同的响应信息。

Burp Suite Sequencer作为Burp Suite中一款检测数据样本随机性质量的工具，通常用于检测访问令牌和密码重置令牌等是否可预测。通过Sequencer的数据样本分析能很好地降低这些关键数据被伪造的风险。

Burp Suite Decoder的功能比较简单，作为Burp Suite中的一款编码/解码工具，它能对原始数据进行各种编码格式和散列的转换。

Burp Suite Comparer在Burp Suite中主要提供一个可视化的差异比对功能，对比分析两次数据之间的区别。
