---
title: "snort入侵检测基础"
date: 2025-07-29 14:55:00
categories:
  - "Security Notes"
tags:
  - "Security"
  - "Linux"
cnblogs_postid: "19010788"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/19010788"
---

实验简介

实验所属系列：网络安全实践

实验对象： 本科/专科信息安全专业

相关课程及专业：计算机基础，Linux基础

实验时数（学分）：2学时

实验类别：实践实验类

预备知识

**入侵检测简介**

入侵检测是指对入侵行为的发现、报警和响应，它通过对计算机网络或计算机系统中的若干关键点收集信息并对其进行分析，从中发现网络或系统中是否有违反安全策略的行为和被攻击的迹象。入侵检测系统（Intrusion Detection System，简称“IDS”）是一种对网络传输进行即时监视，在发现可疑传输时发出警报或者采取主动反应措施的网络安全设备。它与其他网络安全设备的不同之处便在于，IDS是一种积极主动的安全防护技术。

入侵检测的功能主要体现在以下几个方面：

1）监视并分析用户和系统的活动

2）核查系统配置和漏洞

3）识别已知的攻击行为并报警

4）统计分析异常行为

5）评估系统关键资源和数据文件的完整性

6）操作系统的审计跟踪管理并识别违反安全策略的用户行为

从技术上，入侵检测可以分为两类：

1）基于特征标识检测（signature-based）

对于基于特征的检测技术来说，首先要定义违背安全策略的事件的特征，如网络数据包的某些头信息。检测主要判别这类特征是否在所收集到的数据中出现。此方法非常类似杀毒软件。

2）基于异常情况检测（anomaly-based）

而基于异常的检测技术则是先定义一组系统“正常”情况的数值，如CPU利用率、内存利用率、文件校验和等（这类数据可以人为定义，也可以通过观察系统、并用统计的办法得出），然后将系统运行时的数值与所定义的“正常”情况比较，得出是否有被攻击的迹象。这种检测方式的核心在于如何定义所谓的“正常”情况。

**Snort****简介**

Snort是一个强大的轻量级的网络入侵检测系统，它具有实时数据流量分析和日志IP网络数据包的能力，能够进行协议分析，对内容搜索或者匹配。它是一个基于特征检测的入侵检测系统。

Snort有三种工作模式：嗅探器、数据包记录器、网络入侵检测系统。

嗅探器模式：仅仅是从网络上读取数据包并作为连续不断的流显示在终端上。

数据包记录器模式：把数据包记录到硬盘上。

网路入侵检测模式：是最复杂的，而且是可配置的。我们可以让snort分析网络数据流以匹配用户定义的一些规则，并根据检测结果采取一定的动作。

  
在使用Snort时，会自动将网卡设置成混杂模式。

实验目的

理解入侵检测的作用和原理，掌握Snort入侵检测规则格式。

实验环境

攻击机(Server)：Kali

目标机(Target)：Centos

工具(Tools)：Snort、daq、PING

实验步骤一

任务描述：了解snort的基本安装配置

**1. snort****安装步骤**

snort安装使用

1）下载并解压安装包

wget http://172.16.1.254/tools/snort-ids-install.zip

unzip snort-ids-install.zip

tar -zxf snort-2.9.18.1.tar.gz

tar -zxf daq-2.0.7.tar.gz

tar -zxf snortrules-snapshot-29181.tar.gz

2）安装daq

首先安装daq所依赖的开发包：

apt-get install -y flex bison libpcap-dev

可能会报错，依赖包安装，缺少哪个依赖包，安装哪个即可。

然后编译安装daq：

cd daq-2.0.7/

./configure && make && make install

3）安装snort

首先安装snort所依赖的软件包：

apt-get install -y libpcre3-dev libdumbnet-dev zlib1g-dev libdaq-dev

然后编译安装snort：

cd snort-2.9.18.1/

./configure -disable-open-appid && make && make install

注意：因实验机器内无网络，因此无法操作以上安装步骤，仅供大家在自己的环境中安装时参考。

实验环境中snort已经安装完毕，snort安装目录：/root/Desktop/snort-2.9.18.1/

**2. snort****配置**

要能正常使用snort的相关功能，还需我们进行以下操作：

1）进入实验机后，打开terminal终端，切换操作目录为Desktop桌面，在桌面有两个压缩包和一个文件夹：

cd /root/Desktop/

![2025新的知识库/Web/蚁景网安系列课程/卓越班渗透系列课程/assets/72b5039f886589baef78731e4ad661f9_MD5.gif](/assets/cnblogs/snort入侵检测基础/3539156-20250729145454329-1807961451.gif)

2）配置snort规则

解压snort规则文件压缩包：

mkdir snortrules

tar zxf snortrules-snapshot-29181.tar.gz -C snortrules

把snortrules下的文件替换到snort安装目录：

cp -r snortrules/* snort-2.9.18.1/

![2025新的知识库/Web/蚁景网安系列课程/卓越班渗透系列课程/assets/b3a2a77fa32ba489799962fbba872116_MD5.gif](/assets/cnblogs/snort入侵检测基础/3539156-20250729145454051-871317057.gif)

3）修改snort配置文件

更改snort规则配置文件中规则文件路径（RULE_PATH），在snort.conf文件的第104行：

切换到snort安装目录：

cd /root/Desktop/snort-2.9.18.1/

使用leafpad打开snort.conf文件：

leafpad etc/snort.conf

修改第104行为：

var RULE_PATH /root/Desktop/snort-2.9.18.1/rules

![2025新的知识库/Web/蚁景网安系列课程/卓越班渗透系列课程/assets/06f13cdc2bc1660035646676c524d41a_MD5.gif](/assets/cnblogs/snort入侵检测基础/3539156-20250729145454427-982429519.gif)

修改第321~323行为：

webroot no

#decompress_swf { deflate lzma } \

#decompress_pdf { deflate }

4）创建snort默认日志文件夹

mkdir /var/log/snort/

**3.** **验证snort安装**

**![2025新的知识库/Web/蚁景网安系列课程/卓越班渗透系列课程/assets/c13254559f8b0159c76d569d6b443b35_MD5.png](/assets/cnblogs/snort入侵检测基础/3539156-20250729145454166-1564231006.png)**

用法：snort 选项 过滤选项

![2025新的知识库/Web/蚁景网安系列课程/卓越班渗透系列课程/assets/a5ff67841652db378112fd76b356dc69_MD5.png](/assets/cnblogs/snort入侵检测基础/3539156-20250729145454113-2086950053.png)

实验步骤二

**任务描述：了解并使用Snort嗅探器模式**

所谓的嗅探器模式就是snort从网络上读出数据包然后显示在你的控制台上。首先，我们从最基本的用法入手。如果你只要把TCP/IP包头信息打印在屏幕上，只需要输入下面的命令：

snort -v

![2025新的知识库/Web/蚁景网安系列课程/卓越班渗透系列课程/assets/97f916b8718183deff836b616fa73387_MD5.gif](/assets/cnblogs/snort入侵检测基础/3539156-20250729145454504-1793111848.gif)

使用这个命令将使snort只输出IP和TCP/UDP/ICMP的包头信息。

如果你要看到应用层的数据，可以使用：

snort -vd

这条命令使snort在输出包头信息的同时显示包的数据信息。

如果你还要显示数据链路层的信息，就使用下面的命令：

snort -vde

![2025新的知识库/Web/蚁景网安系列课程/卓越班渗透系列课程/assets/81a824e7a789e475d70b6160840bc451_MD5.gif](/assets/cnblogs/snort入侵检测基础/3539156-20250729145455461-1392280547.gif)

注意这些选项开关还可以分开写或者任意结合在一块。例如：下面的命令就和上面最后的一条命令等价：

snort -d -v -e

实验步骤三

**任务描述：了解并使用Snort数据包记录器工作模式**

如果要把所有的包记录到硬盘上，你需要指定一个日志目录，snort就会自动记录数据包：

注意：Ctrl + c，停止记录

mkdir logs

snort -dev -l logs

![2025新的知识库/Web/蚁景网安系列课程/卓越班渗透系列课程/assets/d0686e43189ce9661098ca3bb61dd212_MD5.gif](/assets/cnblogs/snort入侵检测基础/3539156-20250729145454691-80173901.gif)

当然，logs目录必须存在，否则snort就会报告错误信息并退出，如果不存在logs目录，可通过mkdir命令创建。当snort在这种模式下运行，它会记录所有看到的包将其放到指定logs目录下的文件中。

为了只对本地网络进行日志记录，你需要给出本地网络：

snort -dev -l logs -h 10.1.1.0/24

![2025新的知识库/Web/蚁景网安系列课程/卓越班渗透系列课程/assets/e7d787ae82cf4ba091ea21b022233b40_MD5.gif](/assets/cnblogs/snort入侵检测基础/3539156-20250729145455204-1723200337.gif)

这个命令告诉snort把进入C类网络10.1.1.0/24的所有包的数据链路、TCP/IP以及应用层的数据记录到目录logs中以snort.log.（时间戳）为文件名的数据文件。

你可以使用任何支持tcpdump二进制格式的嗅探器程序从这个文件中读出数据包，例如： tcpdump或者Ethereal。使用-r功能开关，也能使snort读出包的数据。snort在所有运行模式下都能够处理tcpdump格式的文件。例如：如果你想在嗅探器模式下把一个tcpdump格式的二进制文件中的包打印到屏幕上，可以输入下面的命令：

snort -r logs/snort.log.1636612831

![2025新的知识库/Web/蚁景网安系列课程/卓越班渗透系列课程/assets/64543f89f114115d7e2a9410fdfc308b_MD5.gif](/assets/cnblogs/snort入侵检测基础/3539156-20250729145454694-335940598.gif)

在日志包和入侵检测模式下，通过BPF（BSD Packet Filter）接口，你可以使用许多方式维护日志文件中的数据。例如，你只想从日志文件中提取TCP包，只需要输入下面的命令行：

snort -r logs/snort.log.1636612831 tcp

![2025新的知识库/Web/蚁景网安系列课程/卓越班渗透系列课程/assets/ce71f879d31cf6092c8fc5a7beb74da7_MD5.gif](/assets/cnblogs/snort入侵检测基础/3539156-20250729145454663-776281906.gif)

实验步骤四

**任务描述：学习使用snort网络入侵检测系统**

**1.** **基本使用**

snort最重要的用途还是作为网络入侵检测系统（NIDS），使用下面命令行可以启动这种模式：

snort -dev -l logs -h 10.1.1.0/24 -c etc/snort.conf

以上命令执行后，所有数据包都会持续输出在终端上，当使用Ctrl + c快捷键时，可以停止运行。

![2025新的知识库/Web/蚁景网安系列课程/卓越班渗透系列课程/assets/afbfc83fabc6478c5869d91db1681720_MD5.gif](/assets/cnblogs/snort入侵检测基础/3539156-20250729145455409-10374498.gif)

注意：如果你想长期使用snort作为自己的入侵检测系统，最好不要使用-v选项。因为使用这个选项，会使snort向屏幕上输出一些信息，会大大降低snort的处理速度，从而在向显示器输出的过程中丢弃一些包。

此外，在绝大多数情况下，也没有必要记录数据链路层的包头，所以-e选项也可以不用：

snort -d -l logs -h 10.1.1.0/24 -c etc/snort.conf

这是使用snort作为网络入侵检测系统最基本的形式，日志中符合规则的包，以ASCII形式保存在有层次的目录结构中。

snort.conf是规则集文件。snort会对每个包和规则集进行匹配，发现这样的包就采取相应的行动。如果你不指定输出目录，snort就输出到/var/log/snort目录。

![2025新的知识库/Web/蚁景网安系列课程/卓越班渗透系列课程/assets/154775655eb4a13c1ac45efa6b383d54_MD5.gif](/assets/cnblogs/snort入侵检测基础/3539156-20250729145454865-1600872163.gif)

**2.** **输出选项**

在NIDS模式下，有很多的方式来配置snort的输出。在默认情况下，snort以ASCII格式记录日志，使用full报警机制。如果使用full报警机制，snort会在包头之后打印报警消息。如果你不需要日志包，可以使用-N选项。

snort有6种报警机制：full、fast、socket、syslog、smb(winpopup)和none。其中有4个可以在命令行状态下使用-A选项设置。这4个是：

-Afast：报警信息包括：一个时间戳(timestamp)、报警消息、源/目的IP地址和端口。

-Afull：是默认的报警模式。

-Aunsock：把报警发送到一个UNIX套接字，需要有一个程序进行监听，这样可以实现实时报警。

-Anone：关闭报警机制。

下面以一个简单例子来对比一下报警信息输出

1）编辑local.rules文件，写入检测规则

leafpad rules/local.rules

alert icmp any any <> $HOME_NET any (logto:"task1";msg:"---ICMP ping---"; sid:100000001)

检测规则简单解释：检测到任何ICMP协议包，都输出消息"---ICMP ping---"。

注意：下个实验，我们会详细学习snort检测规则组成及其编写，这里就不过多解释。

![2025新的知识库/Web/蚁景网安系列课程/卓越班渗透系列课程/assets/c027dac18842b2cc39cc154e95f00ba1_MD5.gif](/assets/cnblogs/snort入侵检测基础/3539156-20250729145454734-1379891849.gif)

2）启动snort，指定为fast模式

snort -d -l logs -c etc/snort.conf -A fast

![2025新的知识库/Web/蚁景网安系列课程/卓越班渗透系列课程/assets/bbcc3757d63f52e5695b93f9a56830e5_MD5.gif](/assets/cnblogs/snort入侵检测基础/3539156-20250729145454717-2040569440.gif)

3）监控报警日志信息，并在另一台机器（client）上执行ping操作，查看报警信息

tail -f logs/alert

ping 10.1.1.100 -c 2

![2025新的知识库/Web/蚁景网安系列课程/卓越班渗透系列课程/assets/38cfc4f601049a9f110eb27acf0d9eb0_MD5.gif](/assets/cnblogs/snort入侵检测基础/3539156-20250729145454611-1620813588.gif)

4）启动snort，指定为full模式，监控报警日志信息，并在另一台机器（client）上执行ping操作，查看并对比报警信息

snort -d -l logs -c etc/snort.conf -A full

![2025新的知识库/Web/蚁景网安系列课程/卓越班渗透系列课程/assets/7313310853b81018c1d867d9b135a356_MD5.gif](/assets/cnblogs/snort入侵检测基础/3539156-20250729145455263-1824893521.gif)

实验报告要求

参考实验原理与相关介绍，完成实验任务，并对实验结果进行分析，完成思考题目，总结实验的心得体会，并提出实验的改进意见。

分析与思考

1. 自己对照snort帮助选项，学习snort选项的功能

2. 在自己本地环境安装snort

3. 对比snort其他输出选项的不同

配套学习资源

http://www.phperz.com/article/15/1205/172953.html
### **一、实验目的**​

1. ​**理解入侵检测核心原理**​：
    - 掌握基于特征（signature-based）和基于异常（anomaly-based）的检测技术差异。
    - 分析入侵检测系统(IDS)在网络安全防护中的主动防御价值。
2. ​**掌握Snort实战应用**​：
    - 完成Snort环境配置与规则部署。
    - 熟练操作三种工作模式：嗅探器、数据包记录器、网络入侵检测系统(NIDS)。
    - 编写并验证自定义检测规则（如ICMP告警规则）。
3. ​**培养安全分析能力**​：
    - 通过报警日志分析网络行为特征。
    - 对比不同输出模式的告警信息差异。

---

### ​**二、实验环境**​

|​**组件**​|​**配置说明**​|
|---|---|
|​**操作系统**​|目标机：CentOS 7；攻击机：Kali Linux|
|​**核心工具**​|Snort 2.9.18.1 + DAQ 2.0.7|
|​**依赖组件**​|libpcap-dev/zlib1g-dev/flex/bison|
|​**网络配置**​|实验网段：10.1.1.0/24|
|​**辅助工具**​|leafpad（文本编辑）、ping（流量触发）|

---

### ​**三、实验内容与要求**​

#### ​**核心原理**​

- ​**基于特征的检测**​：通过预定义规则（如`local.rules`中的ICMP规则）匹配数据包内容。
- ​**Snort工作模式**​：
    - ​**嗅探器模式**​：实时解析数据包头（`-v`/`-d`/`-e`选项）
    - ​**记录器模式**​：保存原始流量包（`-l`指定日志目录）
    - ​**NIDS模式**​：加载规则集（`-c snort.conf`）进行入侵检测

#### ​**实验要求**​

1. 完成Snort环境配置，修复规则路径问题。
2. 测试三种工作模式的操作流程。
3. 编写ICMP检测规则并验证告警功能。
4. 对比fast/full两种告警输出模式差异。

---

### ​**四、实验过程与分析**​

#### ​**关键步骤记录**​

1. ​**环境配置（故障点修复）​**​
    
    bash
    
    复制
    
    ```bash
    # 解压规则库至Snort目录
    tar zxf snortrules-snapshot-29181.tar.gz -C snort-2.9.18.1/
    # 修改配置路径（关键修复）
    leafpad etc/snort.conf  # 第104行：var RULE_PATH /root/Desktop/snort-2.9.18.1/rules
    ```
    
2. ​**嗅探器模式测试**​
    
    bash
    
    复制
    
    ```bash
    snort -v  # 仅显示IP/TCP头信息
    snort -vd  # 增加应用层数据
    snort -vde # 包含数据链路层信息
    ```
    
    ​**输出对比**​：  
    `-vde`模式可解析MAC地址（如`00:0C:29:XX:XX:XX`）
    
3. ​**NIDS模式告警测试**​
    
    - ​**规则编写**​：
        
        bash
        
        复制
        
        ```bash
        alert icmp any any <> $HOME_NET any (msg:"---ICMP ping---"; sid:100000001)
        ```
        
    - ​**告警触发**​：
        
        bash
        
        复制
        
        ```bash
        # Kali攻击机执行
        ping 10.1.1.100 -c 3
        ```
        
    - ​**输出对比**​：
        
        |​**模式**​|​**告警内容**​|​**优势**​|
        |---|---|---|
        |`-A fast`|精简时间戳+IP+消息（0.2ms处理延迟）|高性能实时监控|
        |`-A full`|含TTL/ID等包头详情（如`ID=54321 TTL=64`）|支持深度取证分析|
        

#### ​**故障排查案例**​

|​**故障现象**​|​**原因分析**​|​**解决方案**​|
|---|---|---|
|规则未触发告警|`snort.conf`未包含`local.rules`|添加`include $RULE_PATH/local.rules`|
|报警日志为空|`-A none`意外关闭告警|检查启动参数|
|BPF过滤失效|语法错误（如缺少协议声明）|修正为`snort -r log.pcap tcp`|

---

### ​**五、实验结果总结**​

#### ​**思考题解答**​

1. ​**Snort高级选项解析**​
    
    - `--alert-before-pass`：优先处理告警规则
    - `-k none`：禁用校验和验证（应对畸形包）
    - `--treat-drop-as-alert`：模拟主动响应
2. ​**本地安装注意事项**​
    
    bash
    
    复制
    
    ```bash
    # Ubuntu示例
    sudo apt install -y libdnet-dev libdaq-dev
    ./configure --enable-sourcefire && make
    ```
    
3. ​**输出模式扩展对比**​
    
    |​**模式**​|​**适用场景**​|​**输出示例**​|
    |---|---|---|
    |​**syslog**​|集中日志管理|发送至`/var/log/syslog`|
    |​**unified2**​|Barnyard2解析|二进制格式（需专用工具解析）|
    |​**console**​|快速调试|实时打印彩色告警到终端|
    

#### ​**实验改进建议**​

1. ​**引入主动响应**​：  
    添加`react`规则自动阻断攻击（如`react: block, msg;`）
2. ​**集成可视化分析**​：  
    使用Snorby或BASE解析unified2日志
3. ​**模拟高级攻击检测**​：  
    测试SQL注入规则：`content:"SELECT"; sid:100000002;`

#### ​**心得体会**​

> 通过本次实验深刻认识到：
> 
> - ​**特征检测的局限性**​：无法识别未知攻击（如0day漏洞），需结合异常检测。
> - ​**规则优化的重要性**​：过度宽泛的规则（如`alert icmp any any`）会引发误报风暴。
> - ​**纵深防御的必要性**​：IDS需与防火墙、SIEM系统联动构建完整防护体系。
## 题目答案
![assets/snort入侵检测基础/file-20250723210102153.png](/assets/cnblogs/snort入侵检测基础/3539156-20250729145454584-2008854535.png)
