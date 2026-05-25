---
title: "ctfshow Web入门1-20 信息搜集"
date: 2025-05-11 08:12:00
categories:
  - "CTF Web"
tags:
  - "CTF"
  - "Web"
  - "ctfshow"
cnblogs_postid: "18870513"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18870513"
---

## web1
F12
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511080806621-516465966.png)

## web2
按f12打不开，但是可以用菜单启动
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511080811291-607230636.png)

## web3
藏在响应包里（看网络看得到）
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511080820090-1764711554.png)

## web4
提示：
总有人把后台地址写入robots，帮黑阔大佬们引路。
打开robots.txt
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511080825681-80790168.png)

访问这个得到flag
## web5
提示是phps源码泄露
所以尝试index.phps
下载之后成功找到flag
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511080831488-2050466924.png)

## web6
提示：解压源码到当前目录，测试正常，收工
所以应该有网站压缩包
**网站主页源码文件名称为 www.zip**
所以输入这个后下载到源代码，打开发现提示
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511080836481-1880266732.png)

打开后发现flag
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511080840813-1879580692.png)

## web7
看提示应该是git泄漏
用dirsearch扫果然扫到了
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511080845524-1058284412.png)

访问获得flag
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511080850407-826218410.png)

## web8
svn泄漏
同样扫
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511080856214-1428372309.png)
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511080859172-546845556.png)

## web9
题目提示应该是vim备份文件
> 以index.php来说，第一次退出后，缓存文件名为 .index.php.swp，第二次退出后，缓存文件名为.index.php.swo,第三次退出后文件名为.index.php.swn
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511080904118-609454188.png)

## web10
cookies
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511080909576-598301229.png)

## web11
nslookup -qt=txt flag.ctfshow.com
但是现在好像进不去了
## web12
扫到admin
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511080915557-1914873189.png)

下面有helpline
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511080920715-1477337991.png)

猜测是密码，访问admin，账号admin密码372619038，进入后成功获得flag
## web13
发现document能点
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511080929507-212119183.png)

点一下进去，发现登陆位置
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511080934474-474795739.png)

登录后获得flag
## web14
提示是editor，那就搜editor
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511080943737-198568650.png)

进入后删除upload后面部分进入编辑器
发现插入附件里有个文件空间，点进去
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511080948614-805704179.png)

发现可以看服务器里有哪些文件
翻到/editor/attached/file/var/www/html/nothinghere/fl000g.txt，所以直接访问试试
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511080953270-937757329.png)

## web15
扫到admin
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511080957316-1166121182.png)

进去，没有密码，点忘记密码看看
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511081001961-162019220.png)

所以去找，发现留的是qq邮箱，所以搜QQ，搜出来是西安
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511081007041-336669422.png)

得到flag
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511081011951-388405161.png)

## web16
扫到探针（我自己之前在字典里加的常见探针）
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511081017410-258554602.png)

进去之后点phpinfo
找到flag
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511081033277-768899594.png)

## web17
扫到备份sql文件
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511081044057-954748048.png)

打开之后找到flag
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511081048763-865622697.png)

## web18
看分数大于100时执行的指令
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511081053623-837684035.png)

转换
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511081059479-159937732.png)
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511081117801-1260177229.png)

## web19
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511081124280-47495307.png)

注释藏着
加密代码
```

    function checkForm(){
        var key = "0000000372619038";
        var iv = "ilove36dverymuch";
        var pazzword = $("#pazzword").val();
        pazzword = encrypt(pazzword,key,iv);
        $("#pazzword").val(pazzword);
        $("#loginForm").submit();
        
    }
    function encrypt(data,key,iv) { //key,iv：16位的字符串
        var key1  = CryptoJS.enc.Latin1.parse(key);
        var iv1   = CryptoJS.enc.Latin1.parse(iv);
        return CryptoJS.AES.encrypt(data, key1,{
            iv : iv1,
            mode : CryptoJS.mode.CBC,
            padding : CryptoJS.pad.ZeroPadding
        }).toString();
    }


```
结合这两个解密
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511081129255-56190758.png)

得到flag
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511081134071-1343046333.png)

## web20
先扫db再扫mdb
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511081139198-1080579669.png)

访问之后下载数据库
找到flag
![image](/assets/cnblogs/ctfshow Web入门1-20 信息搜集/3539156-20250511081143841-2077227638.png)
