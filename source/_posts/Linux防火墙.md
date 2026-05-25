---
title: "Linux防火墙"
date: 2025-07-29 14:55:00
categories:
  - "Security Notes"
tags:
  - "Security"
  - "Linux"
cnblogs_postid: "19010786"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/19010786"
---

实验简介  
实验所属系列：防火墙技术  
  
实验对象：本科/专科信息安全专业  
  
相关课程及专业：信息网络安全概论  
  
实验时数（学分）：4学时  
  
实验类别：实践实验类  
  
实验目的  
通过该实验了解Linux防火墙iptables实现原理，掌握iptables基本使用方法，能够利用iptables对操作系统进行加固。  
  
预备知识  
基本原理  
  
netfilter/iptables（简称为iptables）组成Linux平台下的包过滤防火墙，具有完成封包过滤、封包重定向和网络地址转换（NAT）等功能。netfilter是Linux 核心中一个通用架构，它提供了一系列的"表"(tables)，每个表由若干"链"(chains)组成，而每条链中可以有一条或数条规则(rule)组成。可以这样来理解，netfilter是表的容器，表是链的容器，而链又是规则的容器。  
  
规则（rules）其实就是网络管理员预定义的条件，规则一般的定义为“如果数据包头符合这样的条件，就这样处理这个数据包”。规则存储在内核空间的信息包过滤表中，这些规则分别指定了源地址、目的地址、传输协议（如TCP、UDP、ICMP）和服务类型（如HTTP、FTP和SMTP）等。当数据包与规则匹配时，iptables就根据规则所定义的方法来处理这些数据包，如放行（accept）、拒绝（reject）和丢弃（drop）等。配置防火墙的主要工作就是添加、修改和删除这些规则。  
  
iptables内置了4个表，即filter表、nat表、mangle表和raw表，分别用于实现包过滤，网络地址转换、包重构（修改）和数据跟踪处理。  
  
链（chains）是数据包传播的路径，每一条链其实就是众多规则中的一个检查清单，每一条链中可以有一条或数条规则。当一个数据包到达一个链时，iptables就会从链中第一条规则开始检查，看该数据包是否满足规则所定义的条件。如果满足，系统就会根据该条规则所定义的方法处理该数据包；否则iptables将继续检查下一条规则，如果该数据包不符合链中任一条规则，iptables就会根据该链预先定义的默认策略来处理数据包。  
  
iptables采用“表”和“链”的分层结构。在REHL4中是三张表五个链。现在REHL5成了四张表五个链了如下：  
  
  
  
系统缺省的表为"filter"，该表中包含了INPUT、FORWARD和OUTPUT 3个链。每一条链中可以有一条或数条规则，每一条规则都是这样定义的“如果数据包头符合这样的条件，就这样处理这个数据包”。当一个数据包到达一个链时，系统就会从第一条规则开始检查，看是否符合该规则所定义的条件: 如果满足,系统将根据该条规则所定义的方法处理该数据包；如果不满足则继续检查下一条规则。最后，如果该数据包不符合该链中任一条规则的话，系统就会根据该链预先定义的策略(policy)来处理该数据包。  
  
数据包在filter表中的流程为：有数据包进入系统时，系统首先根据路由表决定将数据包发给哪一条链，则可能有三种情况：  
  
1.如果数据包的目的地址是本机，则系统将数据包送往INPUT链，如果通过规则检查，则该包被发给相应的本地进程处理；如果没通过规则检查，系统就会将这个包丢掉；  
  
2.如果数据包的目的地址不是本机，也就是说，这个包将被转发，则系统将数据包送往FORWARD链，如果通过规则检查，则该包被发给相应的本地进程处理；如果没通过规则检查，系统就会将这个包丢掉；  
  
3.如果数据包是由本地系统进程产生的，则系统将其送往OUTPUT链，如果通过规则检查，则该包被发给相应的本地进程处理；如果没通过规则检查，系统就会将这个包丢掉。  
  
iptables执行流程图  
  
如下图所示，iptables在处理数据包时，将按照下面流程执行：  
  
  
  
①当一个数据包进入网卡时，它首先进入PREROUTING链，内核根据数据包目的IP判断是否需要转送出去。  
  
②如果数据包就是进入本机的，它就会沿着图向下移动，到达INPUT链。数据包到了INPUT链后，任何进程都会收到它。本机上运行的程序可以发送数据包，这些数据包会经过OUTPUT链，然后到达POSTROUTING链输出。  
  
③如果数据包是要转发出去的，且内核允许转发，数据包就会如图所示向右移动，经过FORWARD链，然后到达POSTROUTING链输出。  
  
iptables表、链说明  
  
规则表  
  
1.filter表——三个链：INPUT、FORWARD、OUTPUT。  
  
作用：过滤数据包  
  
内核模块：iptables_filter  
  
2.Nat表——三个链：PREROUTING、POSTROUTING、OUTPUT  
  
作用：用于网络地址转换（IP、端口）  
  
内核模块：iptable_nat  
  
3.Mangle表——五个链：PREROUTING、POSTROUTING、INPUT、OUTPUT、FORWARD  
  
作用：修改数据包的服务类型、TTL、并且可以配置路由实现QOS  
  
内核模块：iptable_mangle  
  
4.Raw表——两个链：OUTPUT、PREROUTING  
  
作用：决定数据包是否被状态跟踪机制处理  
  
内核模块：iptable_raw  
  
规则链  
  
1.INPUT——进来的数据包应用此规则链中的策略；  
  
2.OUTPUT——外出的数据包应用此规则链中的策略；  
  
3.FORWARD——转发数据包时应用此规则链中的策略；  
  
4.PREROUTING——对数据包作路由选择前应用此链中的规则；  
  
5.POSTROUTING——对数据包作路由选择后应用此链中的规则。  
  
规则表之间的优先顺序：  
  
规则表之间按照Raw、mangle、nat、filter的顺序进行过滤，具体分三种情况：  
  
第一种情况：入站数据流向  
  
从外界到达防火墙的数据包，先被PREROUTING规则链处理（是否修改数据包地址等），之后会进行路由选择（判断该数据包应该发往何处），如果数据包的目标主机是防火墙本机（比如说Internet用户访问防火墙主机中的web服务器的数据包），内核将其传给INPUT链进行处理（决定是否允许通过等），通过以后再交给系统上层的应用程序（比如Apache服务器）进行响应。  
  
第二种情况：转发数据流向  
  
来自外界的数据包到达防火墙后，首先被PREROUTING规则链处理，之后会进行路由选择，如果数据包的目标地址是其它外部地址（比如局域网用户通过网关访问QQ站点的数据包），则内核将其传递给FORWARD链进行处理（是否转发或拦截），然后再交给POSTROUTING规则链（是否修改数据包的地址等）进行处理。  
  
第三种情况：出站数据流向  
  
防火墙本机向外部地址发送的数据包（比如在防火墙主机中测试公网DNS服务器时），首先被OUTPUT规则链处理，之后进行路由选择，然后传递给POSTROUTING规则链（是否修改数据包的地址等）进行处理。  
  
  
  
iptables语法  
  
  
语法：iptables [-t table] command [match] [-j target/jump]  
  
1）[-t table] 指定规则表  
  
-t 参数用来，内建的规则表有三个，分别是：nat、mangle 和 filter，当未指定规则表时，则一律视为是 filter。个规则表的功能如下：  
  
nat：此规则表拥有 PREROUTING 和 POSTROUTING 两个规则链，主要功能为进行一对一、一对多、多对多等网址转换工作（SNAT、DNAT），这个规则表除了作网址转换外，请不要做其它用途。  
  
mangle：此规则表拥有 PREROUTING、FORWARD 和 POSTROUTING 三个规则链。除了进行网址转换工作会改写封包外，在某些特殊应用可能也必须去改写封包（TTL、TOS）或者是设定markMARK（将封包作记号，以进行后续的过滤），这时就必须将这些工作定义在 mangle 规则表中，由于使用率不高，这里不讨论 mangle 的用法。  
  
filter：这个规则表是默认规则表，拥有 INPUT、FORWARD 和 OUTPUT 三个规则链，这个规则表顾名思义是用来进行封包过滤的处理动作（例如：DROP、 LOG、 ACCEPT 或 REJECT），需要将基本规则都建立在此规则表中。  
  
2）command 常用命令列表：  
  
命令：-A, --append；范例：iptables -A INPUT ...；说明：新增规则到某个规则链中，该规则将会成为规则链中的最后一条规则。  
  
命令：-D, --delete；范例：iptables -D INPUT --dport 80 -j DROP，iptables -D INPUT 1；说明：从某个规则链中删除一条规则，可以输入完整规则，或直接指定规则编号加以删除。  
  
命令：-R, --replace；范例：iptables -R INPUT 1 -s 192.168.0.1 -j DROP；说明：取代现行规则，规则被取代后并不会改变顺序。  
  
命令：-I, --insert；范例：iptables -I INPUT 1 --dport 80 -j ACCEPT；说明：插入一条规则，原本该位置上的规则将会往后移动一个顺位。  
  
命令：-L, --list；范例1 ：iptables -L INPUT，说明： 列出某规则链中的所有规则；范例2：iptables -t nat -L ，说明：列出nat表所有链中的所有规则。  
  
命令：-F, --flush；范例：iptables -F INPUT；说明：删除filter表中INPUT链的所有规则。  
  
命令：-Z, --zero；范例：iptables -Z INPUT；说明：将封包计数器归零。封包计数器是用来计算同一封包出现次数，是过滤阻断式攻击不可或缺的工具。  
  
命令：-N, --new-chain；范例：iptables -N allowed；说明：定义新的规则链。  
  
命令：-X, --delete-chain；范例：iptables -X allowed；说明：删除某个规则链。  
  
命令： -P, --policy；范例：iptables -P INPUT DROP；说明：定义过滤政策。 也就是未符合过滤条件之封包， 默认的处理方式。  
  
命令：-E, --rename-chain；范例：iptables -E allowed disallowed；说明：修改某自定义规则链的名称。  
  
3）[match] 常用封包匹配参数  
  
参数：-p, --protocol；范例：iptables -A INPUT -p tcp；说明：匹配通讯协议类型是否相符，可以使用 ! 运算符进行反向匹配，例如：-p !tcp，意思是指除 tcp 以外的其它类型，如udp、icmp等；如果要匹配所有类型，则可以使用 all 关键词，例如：-p all。  
  
参数：-s, --src, --source；范例：iptables -A INPUT -s 192.168.1.1；说明：用来匹配封包的来源 IP，可以匹配单机或网络，匹配网络时请用数字来表示 子网掩码，例如：-s 192.168.0.0/24，匹配 IP 时可以使用 ! 运算符进行反向匹配，例如：-s !192.168.0.0/24。  
  
参数：-d, --dst, --destination；范例：iptables -A INPUT -d 192.168.1.1；说明：用来匹配封包的目的地 IP，设定方式同上。  
  
参数：-i, --in-interface；范例：iptables -A INPUT -i eth0；说明：用来匹配封包是从哪块网卡进入，可以使用通配字符 + 来做大范围匹配，例如：-i eth+ 表示所有的 ethernet 网卡，也可以使用 ! 运算符进行反向匹配，例如：-i !eth0。  
  
参数：-o, --out-interface；范例：iptables -A FORWARD -o eth0；说明：用来匹配封包要从哪 块网卡送出，设定方式同上。  
  
参数：--sport, --source-port；范例：iptables -A INPUT -p tcp --sport 22；说明：用来匹配封包的源端口，可以匹配单一端口，或是一个范围，例如：--sport 22:80表示从 22 到 80 端口之间都算是符合条件，如果要匹配不连续的多个端口，则必须使用 --multiport 参数，详见后文。匹配端口号时，可以使用 ! 运算符进行反向匹配。  
  
参数：--dport, --destination-port；范例：iptables -A INPUT -p tcp --dport 22；说明：用来匹配封包的目的地端口号，设定方式同上  
  
参数：--tcp-flags；范例：iptables -p tcp --tcp-flags SYN,FIN,ACK SYN；说明：匹配 TCP 封包的状态标志，参数分为两个部分，第一个部分列举出想 匹配的标志，第二部分则列举前述标志中哪些有被设置，未被列举的标志必须是空的。TCP 状态标志包括：SYN（同步）、ACK（应答）、FIN（结束）、RST（重设）、URG（紧急） 、PSH（强迫推送） 等均可使用于参数中，除此之外还可以使用关键词 ALL 和 NONE 进行匹配。匹配标志时，可以使用 ! 运算符行反向匹配。  
  
参数：--syn；范例：iptables -p tcp --syn；说明：用来表示TCP通信协议中，SYN位被打开，而ACK与FIN位关闭的分组，即TCP的初始连接，与 iptables -p tcp --tcp-flags SYN,FIN,ACK SYN 的作用完全相同，如果使用 !运算符，可用来 匹配非要求连接封包。  
  
参数：-m multiport --source-port；范例：iptables -A INPUT -p tcp -m multiport --source-port 22,53,80,110；说明：用来匹配不连续的多个源端口，一次最多可以匹配 15 个端口，可以使用 ! 运算符进行反向匹配。  
  
参数：-m multiport --destination-port；范例：iptables -A INPUT -p tcp -m multiport --destination-port 22,53,80,110；说明：用来匹配不连续的多个目的地端口号，设定方式同上。  
  
参数：-m multiport --port；范例：iptables -A INPUT -p tcp -m multiport --port 22,53,80,110；说明：这个参数比较特殊，用来匹配源端口和目的端口号相同的封包，设定方式同上。注意：在本范例中，如果来源端口号为 80目的地端口号为 110，这种封包并不算符合条件。  
  
参数：--icmp-type；范例：iptables -A INPUT -p icmp --icmp-type 8；说明：用来匹配 ICMP 的类型编号，可以使用代码或数字编号来进行 匹配。请打 iptables -p icmp --help 来查看有哪些代码可用。  
  
参数：-m limit --limit；范例：iptables -A INPUT -m limit --limit 3/hour；说明：用来匹配某段时间内封包的平均流量，上面的例子是用来 匹配：每小时平均流量是否超过一次 3 个封包。 除了每小时平均次外，也可以每秒钟、每分钟或每天平均一次，默认值为每小时平均一次，参数如后： /second、 /minute、/day。 除了进行封 包数量的匹配外，设定这个参数也会在条件达成时，暂停封包的匹配动作，以避免因骇客使用洪水攻击法，导致服务被阻断。  
  
参数：--limit-burst；范例：iptables -A INPUT -m limit --limit-burst 5；说明：用来匹配瞬间大量封包的数量，上面的例子是用来匹配一次同时涌入的封包是否超过 5 个（这是默认值），超过此上限的封包将被直接丢弃。使用效果同上。  
  
参数：-m mac --mac-source；范例：iptables -A INPUT -m mac --mac-source 00:00:00:00:00:01；说明：用来匹配封包来源网络接口的硬件地址，这个参数不能用在 OUTPUT 和 POSTROUTING 规则链上，这是因为封包要送到网 卡后，才能由网卡驱动程序透过 ARP 通讯协议查出目的地的 MAC 地址，所以 iptables 在进行封包匹配时，并不知道封包会送到哪个网络接口去。  
  
参数：--mark；范例：iptables -t mangle -A INPUT -m mark --mark 1；说明：用来匹配封包是否被表示某个号码，当封包被匹配成功时，可以透过 MARK 处理动作，将该封包标示一个号码，号码最大不可以超过 4294967296。  
  
参数：-m owner --uid-owner；范例：iptables -A OUTPUT -m owner --uid-owner 500；说明：用来匹配来自本机的封包，是否为某特定使用者所产生的，这样可以避免服务器使用 root 或其它身分将敏感数据传送出，可以降低系统被骇的损失。可惜这个功能无法 匹配出来自其它主机的封包。  
  
参数：-m owner --gid-owner；范例：iptables -A OUTPUT -m owner --gid-owner 0；说明：用来匹配来自本机的封包，是否为某特定使用者群组所产生的，使用时机同上。  
  
参数：-m owner --pid-owner；范例：iptables -A OUTPUT -m owner --pid-owner 78；说明：用来匹配来自本机的封包，是否为某特定进程所产生的，使用时机同上。  
  
参数：m owner --sid-owner；范例：iptables -A OUTPUT -m owner --sid-owner 100；说明：用来匹配来自本机的封包，是否为某特定 连接（Session ID）的响应封包，使用时机同上。  
  
参数：-m state --state；范例：iptables -A INPUT -m state --state RELATED,ESTABLISHED；说明：用来匹配连接状态， 连接状态共有四种：INVALID、ESTABLISHED、NEW 和 RELATED。  
  
INVALID 表示该封包的连接编号（Session ID）无法辨识或编号不正确。  
  
ESTABLISHED 表示该封包属于某个已经建立的连接。  
  
NEW 表示该封包想要起始一个连接（重设连接或将连接重导向）。  
  
RELATED 表示该封包是属于某个已经建立的连接，所建立的新连接。例如：FTP-DATA 连接必定是源自某个 FTP 连接。  
  
4）[-j target/jump] 常用的处理动作：  
  
-j 参数用来指定要进行的处理动作，常用的处理动作包括：ACCEPT、REJECT、DROP、REDIRECT、MASQUERADE、LOG、DNAT、SNAT、MIRROR、QUEUE、RETURN、MARK，分别说明如下：  
  
ACCEPT： 将封包放行，进行完此处理动作后，将不再匹配其它规则，直接跳往下一个规则链（natostrouting）。  
  
REJECT： 拦阻该封包，并传送封包通知对方，可以传送的封包有几个选择：ICMP port-unreachable、ICMP echo-reply 或是tcp-reset（这个封包会要求对方关闭 连接），进行完此处理动作后，将不再匹配其它规则，直接中断过滤程序。 范例如下：iptables -A FORWARD -p TCP --dport 22 -j REJECT --reject-with tcp-reset  
  
DROP： 丢弃封包不予处理，进行完此处理动作后，将不再匹配其它规则，直接中断过滤程序。  
  
REDIRECT： 将封包重新导向到另一个端口（PNAT），进行完此处理动作后，将会继续匹配其它规则。 这个功能可以用来实现透明代理或用来保护 web 服务器。例如：iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8080  
  
MASQUERADE： 改写封包来源 IP 为防火墙 NIC IP，可以指定 port 对应的范围，进行完此处理动作后，直接跳往下一个规则 链（manglepostrouting）。这个功能与SNAT 略有不同，当进行 IP 伪装时，不需指定要伪装成哪个 IP，IP会从网卡直接读取，当使用拨 号接连时，IP通常是由ISP公司的DHCP 服务器指派的，这个时候 MASQUERADE 特别有用。范例如下：iptables -t nat -A POSTROUTING -p TCP -j MASQUERADE --to-ports 1024-31000  
  
LOG： 将封包相关讯息纪录在 /var/log 中，详细位置请查阅 /etc/syslog.conf 配置文件，进行完此处理动作后，将会继续匹配其规则。例如：iptables -A INPUT -p tcp -j LOG --log-prefix "INPUT packets"  
  
SNAT： 改写封包来源 IP 为某特定 IP 或 IP 范围，可以指定 port 对应的范围，进行完此处理动作后，将直接跳往下一个规则（mangleostrouting）。范例如下：iptables -t nat -A POSTROUTING -p tcp -o eth0 -j SNAT --to-source 194.236.50.155-194.236.50.160:1024-32000  
  
DNAT： 改写封包目的地 IP 为某特定 IP 或 IP 范围，可以指定 port 对应的范围，进行完此处理动作后，将会直接跳往下一个规则链（filter:input 或 filter:forward）。范例如下：iptables -t nat -A PREROUTING -p tcp -d 15.45.23.67 --dport 80 -j DNAT --to-destination 192.168.1.1-192.168.1.10:80-100  
  
MIRROR： 镜射封包，也就是将来源 IP 与目的地 IP 对调后，将封包送回，进行完此处理动作后，将会中断过滤程序。  
  
QUEUE： 中断过滤程序，将封包放入队列，交给其它程序处理。通过自行开发的处理程序，可以进行其它应用，例如：计算连接费用等。  
  
RETURN： 结束在目前规则链中的过滤程序，返回主规则链继续过滤，如果把自定义规则链看成是一个子程序，这个动作则就相当于提前结束子程序并返回到主程序中。  
  
MARK： 将封包标上某个代号，以便提供作为后续过滤的条件判断依据，进行完此处理动作后，将会继续匹配其它规则。范例如下：iptables -t mangle -A PREROUTING -p tcp --dport 22 -j MARK --set-mark 2  
  
  
  
netstat语法  
  
  
NETSTAT [-a] [-b] [-e] [-n] [-o] [-p proto] [-r] [-s] [-v] [interval]  
  
Netstat命令用于显示各种网络相关信息，如网络连接，路由表，接口状态 (Interface Statistics)，masquerade 连接，多播成员 (Multicast Memberships) 等等。  
  
-a   （all）显示所有选项，默认不显示LISTEN相关  
  
-t   （tcp）仅显示tcp相关选项  
  
-u   （udp）仅显示udp相关选项  
  
-n   拒绝显示别名，能显示数字的全部转化成数字  
  
-l   仅列出有在 Listen (监听) 的服務状态  
  
-p   显示建立相关链接的程序名  
  
-r   显示路由信息，路由表  
  
-e   显示扩展信息，例如uid等  
  
-s   按各个协议进行统计  
  
-c   每隔一个固定时间，执行该netstat命令  
  
提示：LISTEN和LISTENING的状态只有用-a或者-l才能看到  
  
1）列出所有端口（包括监听和未监听的）  
  
列出所有端口 netstat -a  
  
列出所有 tcp 端口 netstat -at  
  
列出所有 udp 端口 netstat -au  
  
2）列出所有处于监听状态的 Sockets  
  
只显示监听端口 netstat -l  
  
只列出所有监听 tcp 端口 netstat -lt  
  
只列出所有监听 udp 端口 netstat -lu  
  
只列出所有监听 UNIX 端口 netstat -lx  
  
3）显示每个协议的统计信息  
  
显示所有端口的统计信息 netstat -s  
  
显示TCP端口的统计信息 netstat -st  
  
显示UDP端口的统计信息 netstat - su  
  
4）在 netstat 输出中显示 PID 和进程名称 netstat -p  
  
netstat -p 可以与其它开关一起使用，就可以添加 “PID/进程名称” 到 netstat 输出中，这样 debugging 的时候可以很方便的发现特定端口运行的程序。  
  
5）在 netstat 输出中不显示主机，端口和用户名（host, port or user）  
  
当不想让主机，端口和用户名显示，使用 netstat -n。将会使用数字代替那些名称。  
  
同样可以加速输出，因为不用进行比对查询。  
  
实验环境  
  
  
服务器：centos6.3，IP地址：10.1.1.112  
  
测试者：win2003，IP地址随机，可自己查看，在本例中为10.1.1.16  
  
实验步骤一  
2013年王小虎同学经过四年的学习，终于从北京某高校毕业了，历经千辛万苦，终于应聘到了北京某大型信息公司，担任网络管理员，负责管理公司的机房与网络，可是网管搞怎么搞，小虎同学有点迷茫了，下班后联系了之前的学长一块吃烧烤，请学长指点迷津……学长喝了一口牛栏山，说：沉住气，Rome was not built in a day，想当好网管，首先学会用iptables这个神器！明天你先学会这几个事情：  
  
1、学会查看系统中iptables中已经有的规则，知道如何关闭和启用这些规则；  
  
2、学会用iptables保护自己的主机，从最简单开始，不让别人用ping到主机或者用ssh访问到主机；  
  
3、学会如何利用iptables防御网络DDos攻击；  
  
4、如果服务器不能关闭ssh，但是又要防止黑客的字典攻击和暴力破解，管理员怎么样用iptables来实现？  
  
你先学会上面四个事情，iptables就算入门了，剩下的下次喝酒告诉你如何用iptables做nat吧。  
  
任务一：学会查看系统中iptables中已经有的规则，掌握如何关闭和启用这些规则  
  
  
1. 利用本机putty程序登录到centos服务器中；  
  
2. 利用windows操作机中桌面上的“putty.exe”程序，登录centos服务器（IP地址：10.1.1.112，用户名：root，密码：123456）  
  
  
  
如果出现证书信任的提示，选择“是”，可以看到能够登录到centos主机，输入给定的用户名与密码，登录进，如下所示  
  
  
  
3. 输入命令，查看iptables状态；  
  
#service iptables status      查看iptables状态  
  
  
  
由图中可以看到在表filter中有三个chain，分别为INPUT、FORWARD和OUTPUT。  
  
4. 关闭10.1.1.112上centos服务器的iptables防火墙，如下：  
  
#service iptables stop  
  
  
  
5. 保存并查看10.1.1.112服务器上iptables规则  
  
在iptables中添加的规则即时生效，但重启后规则将会丢失，因此需要保存规则，以便重启时重新加载。  
  
#/etc/init.d/iptables  save  
  
  
  
实验步骤二  
学会用iptables保护自己的主机，不让别人用ping  
  
  
1、清空centos主机中iptables规则：  
  
#iptables -F  
  
  
  
2、登录到windows操作机中，利用ping命令访问10.1.1.112；  
  
  
  
3、在主机centos中，加入对应的规则对centos服务器进行加固，使windows操作机中的无法ping通centos主机。在主机centos中，加入下列规则，并查看。  
  
#iptables -A INPUT -p icmp -j DROP  
  
  
  
发现规则已经生效，无法ping通centos：  
  
  
  
命令说明如下：  
  
-A INPUT   #表示在链INPUT中增加一条规则；  
  
-p icmp   #p指protocol（协议），指对icmp协议进行操作；  
  
-j DROP   #指动作为DROP（丢弃）。  
  
   
  
学会REJECT参数，并理解其与DROP两者的区别  
  
  
在上个任务中，已经使用iptables的DROP处理使windows不能够ping通centos主机；接下来，在centos主机中增加什么样的iptables规则对centos服务器进行加固，能使windows操作机中的ping命令达到下面效果？  
  
现在再试试用REJECT处理。首先，删除刚才所加的规则。  
  
6. 在centos主机中，输入下列命令删除iptables中的规则  
  
# iptables  -F  
  
2. 在centos主机中，加入下列新的iptables规则。  
  
#iptables -A INPUT -p icmp -j REJECT  
  
再次用Windows来ping，结果如下所示：  
  
  
  
与之前DROP处理不一样，ping操作返回Destination port unreachable。  
  
实验步骤三  
如何利用iptables防御网络DDos攻击  
  
1、在centos主机中，输入命令# iptables  -F，删除iptables中的规则  
  
2、在windows操作机下下载attack攻击程序  
  
下载地址：http://tools.yijinglab.com/tools/attack/attack.zip  
  
3、双击运行windows操作机运行攻击工具attack.exe对centos发起洪水攻击；  
  
  
  
4、利用putty工具登录centos主机，输入命令：netstat -an，观察centos服务器资源与网络相关情况，发现大量对centos服务器10.1.1.112的111端口（rpc端口）的访问。  
  
  
  
5、继续输入命令：netstat -st，观察centos服务器TCP统计信息，发现centos服务器短时间收到大量数据包。  
  
  
  
6、由此判断，有攻击者进行对端口111（sunrpc）的tcp洪水攻击，并且攻击者伪装了攻击源IP地址，因此对111端口的tcp协议进行iptables规则设置：iptables -A INPUT -p tcp --dport 111 -j DROP，并查看  
  
  
  
7、在centos服务器的iptables中输入规则之后，等待2分钟左右（centos回收资源需要一定时间），运行相关查看系统网络信息，观察洪水攻击造成的影响；  
  
  
  
8、请一定记住完成上一步之后，关闭windows操作机中的attack命令窗口，停止洪水攻击。  
  
实验步骤四  
如何利用iptables的recent模块防御ssh字典攻击  
  
在某服务器应用中，为了远程管理，SSH不能停掉，但是又要防止攻击者的字典攻击，试通过iptables配置，保证SSH的安全。  
  
iptables的recent模块可以根据源地址、目的地址对最近一段时间内经过本机的数据包的情况进行统计，并根据相应的规则执行，命令如下：  
  
--name   #设定列表名称，默认DEFAULT  
  
--rsource   #源地址，此为默认  
  
--rdest   #目的地址  
  
--seconds   #指定时间内  
  
--hitcount   #命中次数  
  
--set   #将地址添加进列表，并更新信息，包含地址加入的时间戳  
  
--rcheck   #检查地址是否在列表，以第一个匹配开始计算时间  
  
--update   #和rcheck类似，以最后一个匹配计算时间  
  
--remove   #在列表里删除相应地址，后跟列表名称及地址  
  
3. 在centos主机中，输入下列命令删除iptables中的规则：  
  
# iptables  -F  
  
2. 依次点击“开始”>>“所有程序”>>“Metasploit”>>“Metasploit Console；打开metasploit界面，等待几分钟出现msf提示符；  
  
  
  
3. 在msf提示符下，输入：use auxiliary/scanner/ssh/ssh_login对metasploit 进行配置  
  
在msf auxiliary(ssh_login)提示符下：  
  
a)输入命令：set RHOSTS 10.1.1.112，设置SSH主机地址；  
  
b)输入命令：set PASS_FILE c:/pass.txt，设置字典文件；  
  
c)输入命令：set USERNAME root，设置破解的帐号名；  
  
d)设置完成后输入run命令运行字典攻击  
  
  
  
4. 利用putty登录centos服务器，查看系统安全日志信息（/var/log/secure），输入命令：cat /var/log/secure，发现大量相同IP地址登录失败信息，分析可能有人进行ssh暴力破解。  
  
  
  
5. 继续输入命令：cat /var/log/secure | grep 10.1.1.16 | wc -l，对该IP地址进行统计，发现来自该IP地址的登录失败次数不停增长。  
  
  
  
6. 在centos服务器上利用iptables的recent模块进行主机加固。输入如下命令：  
  
a）iptables -A INPUT -p tcp --dport 22 -m state --state NEW -m recent --name SSHPOOL --update --seconds 60 --hitcount 3 -j DROP  
  
b）iptables -A INPUT -p tcp --dport 22 -m state --state NEW -m recent --name SSHPOOL --set -j ACCEPT  
  
规则过程分析：模拟一下某个电脑连接本机SSH服务的数据包流程，假设以下数据包是在一小时内到达本机的：  
  
•当这个电脑的第1个SSH包到达本机，规则a检查SSHPOOL列表中这个源IP是否有hitcount，因为是第一个包，显而易见，列表是0，规则a判定这个数据包不必执行DROP，并且也不处理这个数据包，将数据包转给下条规则；  
  
•规则b将这个数据包计入SSHPOOL列表，就是做+1，因为规则中有-j ACCEPT，规则b放行这个包；  
  
•当第2个SSH包到达本机，规则a检查SSHPOOL列表的hitcount，发现没有超过3，于是判定不执行DROP并转给下条规则处理；  
  
•规则b在SSHPOOL中+1，并放行，第2个数据包进入本机；  
  
•第3个数据包过程如上；  
  
•第4个包到达本机，规则a检查SSHPOOL列表中的hitcount，发现是3了已经连接3次了，于是执行DROP，不必再转给下条规则了丢弃该包。  
  
从上面的流程可以看出，--set的功能在于计录数据包，将源IP加入列表。--update的功能在于判定数据包在seconds和hitcount条件下是否要DROP。  
  
  
  
7. 返回Windows操作机中，查看metasploit，发现SSH暴力破解由于连接错误终止。  
  
  
  
实验报告要求  
参考实验原理与相关介绍，完成实验任务，并对实验结果进行分析，完成思考题目，总结实验的心得体会，并提出实验的改进意见。  
  
分析与思考  
1、写出实验完成过程，并回答实验任务的相关问题。  
  
2、输入其他什么命令，执行结果与“#service iptables status”一样？  
  
3、一个服务器禁ping会不会带来安全性，为什么？  
  
4、如何禁止192.168.2.0网段所有的主机ssh到centos服务器？  
  
5、如何利用iptables的recent模块防御ssh字典攻击，请详细描述防御思路与相关命令。  
  


完整的实验报告结构化内容：

---

### ​**一、实验目的**​

1. 掌握Linux防火墙`iptables`的基本工作原理与规则管理
2. 学会使用`iptables`实现主机安全加固（禁ping、SSH防护）
3. 运用`iptables`防御DDoS攻击和SSH暴力破解
4. 理解防火墙规则表（filter/nat/mangle/raw）与链（INPUT/FORWARD/OUTPUT等）的关系
5. 掌握`netstat`命令分析网络状态的方法

---

### ​**二、实验环境**​

| ​**组件**​ | ​**配置说明**​                   |
| -------- | ---------------------------- |
| 操作系统     | CentOS 6.3（服务器端）             |
| 测试机      | Windows Server 2003（客户端）     |
| 网络工具     | Putty（远程连接）、Metasploit（渗透测试） |
| 攻击工具     | attack.exe（DDoS模拟）           |
| IP地址     | 服务器：10.1.1.112，客户端：10.1.1.16 |

---

### ​**三、实验内容与要求**​

#### ​**原理分析**​

- ​**iptables架构**​：四表五链（filter/nat/mangle/raw表 + INPUT/FORWARD/OUTPUT/PREROUTING/POSTROUTING链）
- ​**封包流程**​：根据目的地址选择路径（本机→INPUT链，转发→FORWARD链，本机发出→OUTPUT链）
- ​**规则语法**​：`iptables [-t 表] 命令 匹配条件 -j 动作`

#### ​**实验要求**​

1. 查看/启停iptables规则，保存配置
2. 实现禁ping（ICMP阻断）并分析DROP与REJECT差异
3. 配置iptables防御SYN洪水攻击
4. 使用recent模块防止SSH字典攻击
5. 完成思考题分析

---

### ​**四、实验过程与分析**​

#### ​**任务1：iptables规则管理**​

```
service iptables status      # 查看规则
service iptables stop        # 关闭防火墙
/etc/init.d/iptables save    # 保存规则
```

​**结果**​：成功查看并操作规则，规则默认存储在`/etc/sysconfig/iptables`。

#### ​**任务2：禁ping实现**​

```
iptables -A INPUT -p icmp -j DROP        # 丢弃ICMP包
iptables -A INPUT -p icmp -j REJECT      # 返回拒绝响应
```

​**对比分析**​：

- ​**DROP**​：客户端持续等待超时（无响应）
- ​**REJECT**​：客户端立即收到`Destination Port Unreachable`（协议拒绝）

#### ​**任务3：防御DDoS攻击**​

1. 模拟攻击：Windows运行`attack.exe`攻击111端口
2. 检测攻击：`netstat -an`发现大量111端口连接
3. 防御命令：
    
    ```
    iptables -A INPUT -p tcp --dport 111 -j DROP
    ```
    

​**效果**​：攻击流量被丢弃，服务器CPU负载恢复正常。

#### ​**任务4：防御SSH暴力破解**​

```
iptables -A INPUT -p tcp --dport 22 -m state --state NEW \
         -m recent --name SSHPOOL --update --seconds 60 --hitcount 3 -j DROP
iptables -A INPUT -p tcp --dport 22 -m state --state NEW \
         -m recent --name SSHPOOL --set -j ACCEPT
```

​**原理**​：

1. 新连接被记录到SSHPOOL列表（`--set`）
2. 60秒内超过3次新连接则触发丢弃（`--update`）
3. Metasploit攻击因频繁失败终止

​**故障排除**​：  
若规则失效，检查：

- `iptables`模块加载：`lsmod | grep xt_recent`
- 时间/次数阈值是否过严（如`--hitcount 3`可调整为5）

---

### ​**五、实验结果总结**​

#### ​**思考题解答**​

1. ​**实验命令等同`service iptables status`**​
    
    ```
    iptables -L -n -v  # 等价命令（需root权限）
    ```
    
2. ​**禁ping的安全影响**​
    - ​**利**​：隐藏主机存在性，防止ICMP扫描
    - ​**弊**​：影响合法网络诊断（需权衡运维需求）
3. ​**封禁192.168.2.0网段SSH**​
    
    ```
    iptables -A INPUT -s 192.168.2.0/24 -p tcp --dport 22 -j DROP
    ```
    
4. ​**recent模块防御逻辑**​
    - 核心：动态记录IP访问频次，超限即阻断
    - 关键参数：`--seconds`（时间窗）、`--hitcount`（阈值）

#### ​**心得体会**​

- iptables通过链式规则实现灵活流量控制，但需深入理解网络协议
- 安全策略需平衡防护强度与可用性（如REJECT比DROP更友好）
- 生产环境中建议结合fail2ban等工具增强自动化防护

#### ​**改进建议**​

1. 增加IPv6环境下iptables6的对比实验
2. 补充防火墙规则备份/恢复的实操环节
3. 引入Wireshark抓包分析验证规则生效过程

---

​**实验结论**​：成功掌握iptables基础防护能力，实现了主机加固与攻击防御，理解了防火墙在企业安全中的核心作用。
## 题目答案
![assets/Linux防火墙/file-20250723210227215.png](/assets/cnblogs/Linux防火墙/3539156-20250729145431391-527068859.png)
