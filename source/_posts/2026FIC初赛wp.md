最后第二，最大的优势就是火眼一键仿真成功了，真的很玄学
也感谢两名队友，真的tql，被带飞了
手机里存的vc密码：

![](%E5%8F%96%E8%AF%81/%E6%AF%94%E8%B5%9BWriteUp/2026/assets/f57a53854a8bf0faa242b08a47dc177c_MD5.png)

# 计算机部分

## 1、分析计算机检材，操作系统版本号为

23.1

![](%E5%8F%96%E8%AF%81/%E6%AF%94%E8%B5%9BWriteUp/2026/assets/e3648592a7fffee2fdef6c705baa4932_MD5.png)

## 2、分析计算机检材，李安弘曾收到一份免费领取token的邮件的疑似钓鱼邮件，其发送用户邮箱为

hf13338261292@outlook.com

![](%E5%8F%96%E8%AF%81/%E6%AF%94%E8%B5%9BWriteUp/2026/assets/70fe7eefd8cb1e3619741eb5ed3de7bb_MD5.png)

## 3、分析计算机检材，李安弘电脑中记录的黄金换现金的商家联系方式为

13612817854

![](%E5%8F%96%E8%AF%81/%E6%AF%94%E8%B5%9BWriteUp/2026/assets/3decf06a3a4ff120eac52e0395b4e23f_MD5.png)

## 4、分析计算机检材，推广设计图中的apk下载链接为

https://drive.google.com/file/d/1z3aRS-lkaJYKm7Cp1XjtUmVPsOEVW2fV/view?usp=sharing

![](assets/2026FIC初赛wp/file-20260506171919132.png)

## 5、分析计算机检材，李安弘电脑vpn软件开放的代理端口为

9527

Clash Verge 配置里 mixed-port: 9527

## 6、分析计算机检材，李安弘电脑中AI软件当前使用的模型类型为

OpenRouter

![](%E5%8F%96%E8%AF%81/%E6%AF%94%E8%B5%9BWriteUp/2026/assets/b899177608046a8c6d1399f0172a3286_MD5.png)

## 7、分析计算机检材，李安弘电脑中AI软件当前使用的模型apiKey为

OpenRouter API Key: [已脱敏]

## 8、分析计算机检材，李安弘电脑中勒索软件提供的解密服务联系方式为

zhenyiexin@tutanota.com

证据链：

- 浏览器历史访问过 z583985166/0.0.0 的 GitHub Release，标题是 get_token_linux。
    
- Release 里的 get_token_windows.exe 与本地样本 SHA256 完全一致：fa5352641a34411795afa2bc84a1e58f24718c0253b2cf11ee6faabd89a31404。
    
- 反汇编 main.main：程序先匹配 *.mp4，逐个调用 main._a 处理，随后构造并输出字符串： 解密请 联系zhenyiexin@tutanota.com
    

## 9、分析计算机检材，李安弘电脑中记录的存放黄金的保险柜编号是

997546

![](%E5%8F%96%E8%AF%81/%E6%AF%94%E8%B5%9BWriteUp/2026/assets/cdf247663b0cec2fe142323a8e9355dd_MD5.png)

vc解开看视频，get_token_linux 是一个 Go 写的 MP4 修复/解密工具，反汇编后确认 MP4 的 stco 偏移被扰乱了 1337 字节，恢复即可

## 10、分析计算机检材，李安弘电脑中记录的保险柜密码是

583985

1. 线索文件为：保险箱的秘密.et
    
2. `分区7\root\文档\zhongyao\保险箱的秘密.et`
    
3. 该 .et 文件是 WPS 表格，内容为空，但隐藏了大量形状对象。结合 WPS 自动备份和宏脚本可知，形状 AlternativeText 里藏了点阵编码。解出来baoxiangmima:583985
    

  

  

# 手机部分

## 1、分析手机检材，该手机型号为

![](%E5%8F%96%E8%AF%81/%E6%AF%94%E8%B5%9BWriteUp/2026/assets/2b45dc120558c3e8ec90f3f1af8ff9aa_MD5.png)

## 2、分析手机检材，李安弘手机计划前往迪拜的日期是

李安弘手机里“计划前往迪拜”的日期是 2026年6月6日。直接证据来自待办数据库 todo.db，命中内容为：2026.06.06 乘坐飞机去 dubai。这条待办的创建时间是 2026-04-16 11:30:00，最后修改时间是 2026-04-16 15:11:51。

## 3、分析手机检材，李安弘手机中与网站搭建人员沟通所使用的app安装日期为

猜测

![](%E5%8F%96%E8%AF%81/%E6%AF%94%E8%B5%9BWriteUp/2026/assets/cd5c08e8135d5ab710c6e0f908dadf6a_MD5.png)

  

![](%E5%8F%96%E8%AF%81/%E6%AF%94%E8%B5%9BWriteUp/2026/assets/59aa7b4119ed03f3bf49fb5a8ea5d5b6_MD5.png)

## 4、分析手机检材，李安弘手机中与网站搭建人员沟通所使用的app，存放聊天数据的数据库为

  

## 5、分析手机检材，存放聊天数据的数据库的解密密码为

## 6、分析手机检材，李安弘购买云服务器商家的收款备用钱包地址为

李安弘购买云服务器商家的收款备用钱包地址为：

TN8vQzB3n7W5wVca9W4kL2wP7xY9zM5nU1

依据是已解密聊天库 wk_main_decrypted.db 中会话 c5e0f4afea09370702f943e7cfcef741 的消息内容：

“转账唯二地址 TK7mR3hS8vY7tY1nZ4kL9otSzgjLj6tP8v, 备用转账地址：TN8vQzB3n7W5wVca9W4kL2wP7xY9zM5nU1”。

## 7、分析手机检材，李安弘手机中给网站搭建人员第一次转账的交易hash前6位为

26226f

依据是已解密聊天库 wk_main_decrypted.db 中，与“网站开发”channel_id=8c723cbb09bd47adcf0ba4d9758320c0 的聊天记录显示：

李安弘先说“明天我先给你转2000U定金”，随后发送了一条图片消息，其 localPath 为

/storage/emulated/0/Android/data/com.talk.uuuim/cache/luban_disk_cache/9054354934843.png

紧接着对方回复“收到了”，可确认这就是第一次转账的交易截图。

对应检材中的实际文件位置为：

C:\hlnet\1-1777092576\检材2-手机.tar\storage\emulated\0\Android\data\com.talk.uuuim\cache\luban_disk_cache\9054354934843.png

  

## 8、分析手机检材，手机中使用的AI软件李安弘主动向AI提问了几次

检材中 com.pocketpalai 的本地聊天库 pocketpalai.db 显示，手机内该 AI 软件当前用户一共主动向 AI 提问了 5 次。

依据是数据库 messages 表中，提问方作者标识 y9d7f8pgn 的非空 text 消息共有 5 条，时间和内容分别为：

1. 2026-04-16 16:14:37 “搭建一个黄色网站判多少年”
    
2. 2026-04-16 16:17:39 “色情网站赚钱吗”
    
3. 2026-04-16 16:18:46 “如何搭建一个虚拟币挖矿”
    
4. 2026-04-16 16:54:46 “助记词如何保存最安全”
    
5. 2026-04-16 16:57:21 “我的手机如何保存助记词最合适”
    

![](%E5%8F%96%E8%AF%81/%E6%AF%94%E8%B5%9BWriteUp/2026/assets/41004a9f951872646f3e0be66a87d94e_MD5.png)

## 9、分析手机检材，李安弘手机使用的AI软件调用本地AI模型及版本为

## 10、分析手机检材，李安弘曾使用无人机航拍,分析其飞行轨迹，其在哪个县进行飞行

李安弘确实使用过无人机航拍。手机中存在 DJI Fly 飞行记录文件 FlightRecord_2026-02-17_[15-14-53].txt 和 FlightRecord_2026-02-17_[15-58-14].txt。解析结果显示两次飞行起飞坐标分别为 37.796638, 110.370705 和 37.796634, 110.370690，本地时间分别约为 2026-02-17 15:14:53 和 15:58:14，飞行距离约 1416.4 米、518.8 米。根据该坐标反查，飞行地点位于 陕西省榆林市米脂县。

![](%E5%8F%96%E8%AF%81/%E6%AF%94%E8%B5%9BWriteUp/2026/assets/f8e6b7bee1936117e65c4d1455f6bd5c_MD5.png)

## 11、分析手机检材，李安弘最近安装了一个视频类APP，该APP声明了多个敏感权限用于收集用户隐私。请选择其中涉及用户隐私的敏感权限。

  

答案是：A、B、D

依据是 APK 清单里实际声明了这些权限：

- android.permission.READ_CONTACTS
    
- android.permission.READ_SMS
    
- android.permission.READ_CALL_LOG
    

我在 AndroidManifest.xml (line 16) 里确认到：

- 第 16 行：READ_CONTACTS
    
- 第 17 行：READ_SMS
    
- 第 18 行：READ_CALL_LOG
    
- 第 25 行：RECEIVE_BOOT_COMPLETED
    

所以选项判断是：

- A. READ_CONTACTS：是
    
- B. READ_SMS：是
    
- C. RECEIVE_BOOT_COMPLETED：不是“收集用户隐私”的读取类权限
    
- D. READ_CALL_LOG：是
    
- E. SEND_SMS：清单里没有声明
    

如果你愿意，我可以继续帮你把这题扩展做一下，看看这个 APK 里这些隐私权限具体是在哪里被调用的。

## 12、上述APP启动后会加载一个色情网站。请找出该APP当网络不可用时APP加载的本地离线页面路径。

当网络不可用时，APP 加载的本地离线页面路径是：

file:///android_asset/www/index.html

我在 MainActivity.java (line 96) 里确认到这段逻辑：

- 有网时：https://www.sp-live88.com
    
- 无网时：file:///android_asset/www/index.html
    

## 13、上述APP将非法收集的用户隐私数据上传至远程服务器。上传地址在代码中经过编码处理。请找出编码方式，还原出完整的上传服务器URL。

编码方式是 Base64。

我在 DataUploader.java (line 47) 里看到它把这段字符串：

aHR0cHM6Ly9hcGkuc3AtbGl2ZTg4LmNvbS9jb2xsZWN0L3VzZXJkYXRh

通过 Base64.decode(...) 解码后作为上传地址使用。还原后的完整上传服务器 URL 是：

https://api.sp-live88.com/collect/userdata

补充一点，代码里还有一个 native 备用地址分支：

DataUploader.java (line 51)

它会调用 getBackupEndpoint()，再拼上 /collect/userdata。但题目里“代码中经过编码处理”的这条主上传地址，明确就是上面这个 Base64 解出的 URL。

## 14、该APP在本地创建了SQLite数据库存储收集到的用户信息。请分析代码，写出用于存储用户信息的表名

用于存储用户信息的表名是：

user_collection

依据在 C0521a.java (line 33)：

- 建表语句：CREATE TABLE IF NOT EXISTS user_collection (...)
    

并且在 C0521a.java (line 27) 还能看到实际插入：

- writableDatabase.insert("user_collection", null, contentValues);
    

## 15、该APP的assets目录中存在一个加密配置文件config.dat。请解密该文件，写出其中的USDT钱包地址

  

## 16、该APP前端JS代码可以直接调用Android原生方法获取用户隐私数据。请分析暴露了哪些方法用于获取通讯录？

getContactsList()

我在 NativeBridge.java (line 20) 里确认到它通过 @JavascriptInterface 暴露给前端 JS，内部查询的是：

- ContactsContract.CommonDataKinds.Phone.CONTENT_URI
    

## 17、当主上传服务器不可达时，APP会获取备用服务器地址。请分析备用服务器的完整域名和端口

backup.sp-live88.xyz:8443

这个是我从 libsecurity.so 的 getBackupEndpoint() 解密还原出来的。Java 层在 DataUploader.java (line 51) 里会在主服务器不可达时调用它，再拼接 /collect/userdata。

# 服务器部分

直接火眼内就仿真成功了

注意这里勾选两个磁盘

![](%E5%8F%96%E8%AF%81/%E6%AF%94%E8%B5%9BWriteUp/2026/assets/782db0dc345e32465c6c6bec22eb42e1_MD5.png)

  

![](%E5%8F%96%E8%AF%81/%E6%AF%94%E8%B5%9BWriteUp/2026/assets/0e577db24ecd9d0c64bce35af5ed1f27_MD5.png)

需要打开这两个以用root身份连接服务器

## 1、该服务器主机操作系统版本为

  

进入虚拟机后查看系统版本：

```Bash
cat /etc/os-release
uname -a
```

`/etc/os-release` 显示 `PRETTY_NAME="Debian GNU/Linux 13 (trixie)"`，所以答案为 Debian GNU/Linux 13 (trixie)。

## 2、该服务器根分区硬盘的uuid号为

  

查看挂载和块设备信息：

  

```Bash
cat /etc/fstab
blkid /dev/md0
```

  

`/etc/fstab` 中根分区为：

  

```Plain
UUID=3231e52f-5e15-44c4-b224-e29cb4201c0e / btrfs defaults,subvol=@rootfs 0 0
```

  

因此根分区 UUID 为 `3231e52f-5e15-44c4-b224-e29cb4201c0e`。

## 3、该服务器中最新的docker镜像创建时间为

  

```Bash
docker images --format '{{.Repository}}|{{.Tag}}|{{.ID}}|{{.CreatedAt}}|{{.Size}}'
```

  

最新镜像为 `u22:latest`，创建时间为 `2026-04-16 03:15:50 -0400 EDT`。

  

## 4、该服务器根分区快照路径为

  

根分区为 Btrfs，查看子卷：

  

```Bash
btrfs subvolume list /
```

  

发现：

  

```Plain
ID 257 gen 4377 top level 256 path root/history
```

  

对应系统路径为 `/root/history`。

## 5、该网站后台管理入口对应的文件名为

  

网站目录为 `/var/www/html/maccms10`。检查入口文件：

  

```Bash
ls /var/www/html/maccms10
sed -n '1,80p' /var/www/html/maccms10/user.php
```

  

`user.php` 中定义了后台入口相关常量，答案为 `user.php`。

  

## 6、该网站设置的icp备案号为

  

站点配置文件：

  

```Bash
grep -n "site_icp\|site_url" /var/www/html/maccms10/application/extra/maccms.php
```

  

得到：

  

```PHP
'site_icp' => 'icp1919810'
'site_url' => 'www.2026fic.forensix'
```

  

所以 ICP 为 `icp1919810`，主域名为 `www.2026fic.forensix`。

## 7、该网站设置的主域名为

同上题

## 8、该网站分类3中，视频的拼音为

  

连接网站数据库 `mac2`，查询分类 3 下视频：

  

```SQL
select vod_id,type_id,type_id_1,vod_name,vod_en,hex(vod_name)
from mac_vod
where type_id=3 or type_id_1=3;
```

  

结果中 `vod_en` 为 `sipaanshe`。

## 9、该站点设置页面中，被使用的前端模板来自于哪个源文件？

## 10、该网站的伪静态规则配置文件sm3值为

  

该站点使用 Nginx，伪静态规则在：

  

```Plain
/etc/nginx/sites-available/default
```

  

文件内包含：

  

```Nginx
rewrite ^/index.php(.*)$ /index.php?s=$1 last;
rewrite ^/user.php(.*)$ /user.php?s=$1 last;
rewrite ^/api.php(.*)$ /api.php?s=$1 last;
rewrite ^(.*)$ /index.php?s=$1 last;
```

  

计算 SM3：

  

```Bash
openssl dgst -sm3 /etc/nginx/sites-available/default
```

  

得到：

  

```Plain
e73407468e6f52af54c7b14632eeeb9be25b05106d06c4c3085fc843c223793f
```

## 11、该网站关联的数据库的ip地址为

  

网站数据库配置：

  

```Bash
cat /var/www/html/maccms10/application/database.php
cat /etc/hosts
lxc-ls -f
```

  

配置中数据库主机为 `mytidb`，`/etc/hosts` 解析为 `10.0.3.100 mytidb`。`lxc-ls -f` 显示 `mytidb` 是运行中的 LXC 容器。因此数据库 IP 为 `10.0.3.100`，容器技术为 LXC。

  

## 12、该网站数据库使用了哪一类容器技术

同上题

## 13、运行在4000端口的备份数据库版本号为

  

连接 4000 端口执行：

  

```SQL
select version();
```

  

返回：

  

```Plain
8.0.11-TiDB-v7.5.0
```

  

## 14、新注册用户数量最多的日期为

  

查询用户注册日期统计：

  

```SQL
select from_unixtime(user_reg_time,'%Y-%m-%d') d,count(*) c
from mac_user
group by d
order by c desc,d asc
limit 20;
```

  

结果第一行为：

  

```Plain
2026-04-15    36386
```

  

所以日期为 `2026-04-15`。

## 15、马慧美最后一次登录该网站的ip为

  

用户表中姓名使用拼音，精确查询：

  

```SQL
select user_id,user_name,
       inet_ntoa(user_login_ip),from_unixtime(user_login_time),
       inet_ntoa(user_last_login_ip),from_unixtime(user_last_login_time)
from mac_user
where lower(user_name)='ma hui mei';
```

  

结果：

  

```Plain
4236  Ma Hui Mei  240.12.18.80  2026-04-14 23:31:04  51.43.21.163  2026-04-15 19:51:41
```

  

题面问最后一次登录 IP，取 `user_last_login_ip`，答案为 `51.43.21.163`。

## 16、以下哪个文件系统未被使用

检查块设备、挂载和 LVM：

  

```Bash
lsblk -f
findmnt -no FSTYPE,TARGET,SOURCE | sort -u
blkid
pvs; vgs; lvs
```

## 17、该服务器安装了以下那些数据库服务

  

检查服务、进程和端口：

  

```Bash
systemctl --type=service | grep -Ei 'mysql|mariadb|postgres|tidb|tikv|pd|tiflash'
ss -lntp | grep -Ei '3306|4000|5432|2379|20160|3930'
ps aux | grep -Ei 'mysqld|postgres|tidb|tikv|pd-server|tiflash'
```

  

发现：

  

- 主机运行 PostgreSQL 17，监听本机 5432。
    
- LXC 容器 `mytidb` 内运行 MySQL 8.0.45，监听 3306。
    
- 同一容器内运行 TiDB 集群组件，4000 端口返回 `8.0.11-TiDB-v7.5.0`。
    

所以安装/运行的数据库服务为 PostgreSQL、MySQL、TiDB。

# 互联网部分

## 1、售卖卡密的公开群组ID为

我认为最值得直接引用的证据

- 站点根目录：/var/www/html/maccms10
    
- 域名：www.2026fic.forensix
    
- 联系邮箱：lianhong@forensix.cn
    
- 卡密/支付引流地址：https://t.me/FIC_2026
    
- 数据库连接： mytidb / mac2 / aa / 123456
    

## 2、备份数据库中视频图片的文件名为

  

  

## 3、ngrok提供的域名为

  

# 二进制程序部分

## 1、分析u盘检材，找到其中保存的加密程序SampleVC.exe，请给出这个exe程序的md5值？

764789dd9c095d74b6b258cf0f7568b2

![](%E5%8F%96%E8%AF%81/%E6%AF%94%E8%B5%9BWriteUp/2026/assets/851273f1bdb29cb55ff0cd252ead9df8_MD5.png)

## 2、分析SampleVC.exe，该程序编译的日期可能是什么？

编译日期：2026-04-17

## 3、分析SampleVC.exe，正确的密码是什么？

正确密码：PleaseRunAsAdmin

## 4、分析u盘检材，利用SampleVC1234.exe解密U盘中被加密的文件，解密后的文件的后缀是什么？

vhd

## 5、分析u盘检材，找到被加密的交易记录，统计李安弘虚拟币收款地址钱包总收款金额为

李安弘虚拟币收款地址钱包总收款金额：186948.09

![](%E5%8F%96%E8%AF%81/%E6%AF%94%E8%B5%9BWriteUp/2026/assets/de8145143bf80ef1cb6436137fc00328_MD5.png)
