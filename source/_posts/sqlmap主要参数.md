---
title: "sqlmap主要参数"
date: 2024-11-18 18:33:00
categories:
  - "CTF Web"
tags:
  - "CTF"
  - "Web"
cnblogs_postid: "18553369"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18553369"
---

# 重要参数
|参数|描述|
|----|----|
| -a, --all | 获取所有信息 |
| -b, --banner | 获取数据库管理系统的标志 |
| -current -user | 获取数据库管理系统的当前用户 |
| -current -db | 获取数据库管理系统的当前数据库 |
| -hostname | 获取数据库服务器的主机名称 |
| -is -dba | 检测DBMS当前用户是否是DBA |
| -users | 枚举数据库管理系统用户 |
| -passwords | 枚举数据库管理系统用户密码的哈希 |
| -privileges | 枚举数据库管理系统用户的权限 |
| -roles | 枚举数据库管理系统用户的角色 |
| -dbs | 数据库系统数据库 |
| -tables | 枚举DBMS数据库中的表 |
| -columns | 枚举数据库架构 |
| -count | 检索表的项目数 |
| -schema | 转储数据库表项 |
| -dump | 转储数据库所有表项 |
| -dump -all | 转储数据库所有项 |
| -search | 搜索列、表和/或数据库名称 |
| -comments | 获取DBMS注释 |
| -D DB | 指定要进行枚举的数据库名 |
| -T TBL | DBMS数据库表枚举 |
| -C COL | DBMS数据库表列枚举 |
| -X EXCLUDECOL | DBMS数据库表不进行枚举 |
| -U USER | 用来进行枚举的数据库用户 |
| -exclude -sysdbs | 枚举表时排除系统数据库 |
| -pivot -column | 枢轴列名称 |
| -where=DUMPWHERE | 使用where条件进行表转储 |
| -start= LIMITSTART | 获取第一个查询的输出数据位置 |
| -stop= LIMITSTOP | 获取最后一个查询的输出数据位置 |
| -first= FIRSTCHAR | 第一个查询输出的字符获取 |
| -last= LASTCHAR | 最后一个查询输出的字符获取 |
| -sql -query= QUERY | 要执行的SQL语句 |
| -sql -shell | 提示交互式SQL的shell |
| -sql -file= SQLFILE | 要执行的SQL文件 |
## 所有参数
|参数|英文|中文|
|----|----|----|
| -h, --help |Show basic help message and exit|显示基本帮助信息并退出|
| -hh |Show advanced help message and exit|显示高级帮助信息并退出|
| --version |Show program's version number and exit|显示程序版本号并退出|
| -v VERBOSE |Verbosity level: 0-6 (default 1)|详细程度级别：0 - 6（默认1）|
| -u URL, --url=URL <br> -g GOOGLEDORK |At least one of these options has to be provided to define the<br>target(s)|必须提供这些选项中的至少一个来定义目标|
| -u URL, --url=URL |Target URL (e.g. "http://www.site.com/vuln.php?id=1")|目标URL（例如 "http://www.site.com/vuln.php?id=1"）|
| -g GOOGLEDORK |Process Google dork results as target URLs|将谷歌搜索指令结果作为目标URL处理|
| --data=DATA |Data string to be sent through POST (e.g. "id=1")|通过POST发送的数据字符串（例如 "id=1"）|
| --cookie=COOKIE |HTTP Cookie header value (e.g. "PHPSESSID=a8d127e..")|HTTP Cookie头部值（例如 "PHPSESSID=a8d127e..")|
| --random-agent |Use randomly selected HTTP User-Agent header value|使用随机选择的HTTP用户代理头部值|
| --proxy=PROXY |Use a proxy to connect to the target URL|使用代理连接到目标URL|
| --tor |Use Tor anonymity network|使用Tor匿名网络|
| --check-tor |Check to see if Tor is used properly|检查Tor是否被正确使用|
| -p TESTPARAMETER |Testable parameter(s)|可测试的参数|
| --dbms=DBMS |Force back-end DBMS to provided value|将后端数据库管理系统强制设置为提供的值|
| --level=LEVEL |Level of tests to perform (1-5, default 1)|要执行的测试级别（1 - 5，默认1）|
| --risk=RISK |Risk of tests to perform (1-3, default 1)|要执行的1测试风险（1 - 3，默认1）|
| --technique=TECH.. |SQL injection techniques to use (default "BEUSTQ")|要使用的SQL注入技术（默认 "BEUSTQ"）|
| -a, --all |Retrieve everything|获取所有内容|
| -b, --banner |Retrieve DBMS banner|获取数据库管理系统的标志|
| --current-user |Retrieve DBMS current user|获取数据库管理系统的当前用户|
| --current-db |Retrieve DBMS current database|获取数据库管理系统的当前数据库|
| --passwords |Enumerate DBMS users password hashes|枚举数据库管理系统用户密码的哈希|
| --dbs |Enumerate DBMS databases|枚举数据库管理系统的数据库|
| --columns |Enumerate DBMS database table columns|枚举数据库管理系统数据库表的列|
| --schema |Enumerate DBMS schema|枚举数据库管理系统的架构|
| --dump |Dump DBMS database table entries|转储数据库管理系统数据库表项|
| --dump-all |Dump all DBMS databases tables entries|转储所有数据库管理系统数据库表的所有项|
| -D DB |DBMS database to enumerate|要枚举的数据库管理系统数据库|
| -T TBL |DBMS database table(s) to enumerate|要枚举的数据库管理系统数据库表|
| -C COL |DBMS database table column(s) to enumerate|要枚举的数据库管理系统数据库表列|
| --os-shell |Prompt for an interactive operating system shell|提示交互式操作系统shell|
| --os-pwn |Prompt for an OOB shell, Meterpreter or VNC|提示获取一个带外（OOB）shell、Meterpreter或VNC|
| --batch |Never ask for user input, use the default behavior|从不询问用户输入，使用默认行为|
| --flush-session |Flush session files for current target|刷新当前目标的会话文件|
| --wizard |Simple wizard interface for beginner users|面向初学者用户的简单向导界面|
| -hostname |Get the hostname of the database server|获取数据库服务器的主机名称|
| -is -dba |Detect whether the current user of the DBMS is a DBA|检测DBMS当前用户是否是DBA|
| -users |Enumerate the users of the database management system|枚举数据库管理系统用户|
| -privileges |Enumerate the privileges of the users of the database management system|枚举数据库管理系统用户的权限|
| -roles |Enumerate the roles of the users of the database management system|枚举数据库管理系统用户的角色|
| -count |Retrieve the number of items in the table|检索表的项目数|
| -search |Search for column, table and/or database names|搜索列、表和/或数据库名称|
| -comments |Get the comments of the DBMS|获取DBMS注释|
| -X EXCLUDECOL |Exclude columns from enumerating in the DBMS database table|DBMS数据库表枚举时排除某些列|
| -U USER |Use the specified user for enumerating in the DBMS|在DBMS中使用指定用户进行枚举|
| -exclude -sysdbs |Exclude system databases when enumerating tables|枚举表时排除系统数据库|
| -pivot -column |Pivot column name|枢轴列名称|
| -where=DUMPWHERE |Use the where condition for dumping table entries|使用where条件转储表项|
| -start= LIMITSTART |Get the position of the output data of the first query|获取第一个查询的输出数据位置|
| -stop= LIMITSTOP |Get the position of the output data of the last query|获取最后一个查询的输出数据位置|
| -first= FIRSTCHAR |Get the characters of the output of the first query|获取第一个查询输出的字符|
| -last= LASTCHAR |Get the characters of the output of the last query|获取最后一个查询输出的字符|
| -sql -query= QUERY |Execute the SQL statement|执行SQL语句|
| -sql -shell |Prompt for an interactive SQL shell|提示交互式SQL shell|
| -sql -file= SQLFILE |Execute the SQL file|执行SQL文件|
