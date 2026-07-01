---
title: "2026PolarEDF夏季赛wp"
date: 2026-06-07 18:00
categories:
  - "Forensics Writeup"
tags:
  - "Forensics"
  - "Writeup"
  - "PolarEDF"
cnblogs_postid: "20361585"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/20361585"
---

<h2>第一部分：PC端</h2>
<h3>PC端1</h3>
<p>本题思路如下：</p>
<p>用ufs生成一个完整e01</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728003.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141223989-1282640395.png"/></p>
<p>然后火眼打开</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728004.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224079-721786958.png"/></p>
<h3>PC端2</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728005.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141223923-2085397.png"/></p>
<h3>PC端3</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728006.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141223972-1434596114.png"/></p>
<h3>PC端4</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728007.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141223828-1324257882.png"/></p>
<h3>PC端5</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728008.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141223976-444679237.png"/></p>
<h3>PC端6</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728009.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141223978-502934597.png"/></p>
<h3>PC端7</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728010.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141223996-938244533.png"/></p>
<h3>PC端8</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728011.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224202-176544271.png"/></p>
<p>然后去找这个数据库</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728012.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141223730-1685115000.png"/></p>
<h3>PC端9</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728013.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141223815-1626411880.png"/></p>
<h3>PC端10</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728014.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224093-83585736.png"/></p>
<h3>PC端11</h3>
<p>本题思路如下：</p>
<h3>PC端12</h3>
<p>本题思路如下：</p>
<p>用随波逐流扫出来压缩包，提取后打开<br/>
<img alt="assets/2026PolarEDF夏季赛/file-20260607135728015.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141223767-1163726303.png"/></p>
<p>给了提示，直接爆破</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728016.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141223818-1219228019.png"/></p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728017.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141223418-1799821467.png"/></p>
<p>打开是冰箱，提示是备案号，去搜就行</p>
<p>注意这里是2024年前的数据</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728018.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141223923-1184671141.png"/></p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728019.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141223673-1697623060.png"/></p>
<h3>PC端13</h3>
<p>本题思路如下：</p>
<p>没时间了直接丢云沙箱</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728020.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224080-216442312.png"/></p>
<h3>PC端14</h3>
<p>本题思路如下：</p>
<p>根据信息写个简单解密代码</p>
<p>from Crypto.Cipher import AES</p>
<p>key = "1234567890123456".ljust(32).encode()</p>
<p>filename="encrypted_classes3.dex"</p>
<p>with open(filename, "rb") as f:</p>
<p>iv = f.read(16)</p>
<p>with open(filename, "rb") as f:</p>
<p>ciphertext = f.read()</p>
<p>cipher = AES.new(key, AES.MODE_CBC, iv)</p>
<p>plaintext = cipher.decrypt(ciphertext)</p>
<p>pad_len = plaintext[-1]</p>
<p>plaintext = plaintext[:-pad_len]</p>
<p>filename="de"+filename[2:]</p>
<p>with open(filename, "wb") as f:</p>
<p>f.write(plaintext)</p>
<p>生成解密的dex</p>
<p>还要把前16字节裁掉</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728021.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141223602-1327763130.png"/></p>
<p>全部解密后在第三部分找到密码和flag信息</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728022.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141223800-630186140.png"/></p>
<h3>PC端15</h3>
<p>本题思路如下：</p>
<p>找到flag位置</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728023.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224106-752074276.png"/></p>
<p>解一下密</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728024.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141223789-959732449.png"/></p>
<h2>第二部分：移动端</h2>
<h3>移动端1</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728025.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224077-1510623006.png"/></p>
<h3>移动端2</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728026.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224635-222859258.png"/></p>
<h3>移动端3</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728027.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224052-2106617320.png"/></p>
<h3>移动端4</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728028.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224146-560626005.png"/></p>
<h3>移动端5</h3>
<p>本题思路如下：</p>
<h3>移动端6</h3>
<p>本题思路如下：</p>
<p>这里被截图骗了</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728029.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224014-441727121.png"/></p>
<p>实际位置应该在软件目录的bash history</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728030.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224120-204841469.png"/></p>
<h3>移动端7</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728031.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141223749-2000139749.png"/></p>
<h3>移动端8</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728032.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224114-1876176038.png"/></p>
<h3>移动端9</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728033.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224091-360685428.png"/></p>
<h3>移动端10</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728034.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141223953-239907169.png"/></p>
<h3>移动端11</h3>
<p>本题思路如下：</p>
<h3>移动端12</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728035.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141223851-1848805637.png"/></p>
<h3>移动端13</h3>
<p>本题思路如下：</p>
<h3>移动端14</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728036.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224010-1135559283.png"/></p>
<h3>移动端15</h3>
<p>本题思路如下：</p>
<h3>移动端16.</h3>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728037.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224034-1078028951.png"/></p>
<h3>移动端17.</h3>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728038.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141223938-1152391269.png"/></p>
<h3>移动端18.</h3>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728039.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224109-499773393.png"/></p>
<h3>移动端19.</h3>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728040.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141223861-1666080749.png"/></p>
<p>说明在libnative-lib.so里，用ida打开直接获取账号密码</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728041.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224054-333139730.png"/></p>
<h3>移动端20.</h3>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728042.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224040-788073654.png"/></p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728043.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224089-1443297657.png"/></p>
<h2>第三部分：服务器端</h2>
<h3>服务器端1</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728044.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224097-660166556.png"/></p>
<h3>服务器端2</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728045.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224017-723045094.png"/></p>
<h3>服务器端3</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728046.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224047-28663502.png"/></p>
<h3>服务器端4</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728047.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224029-1757882484.png"/></p>
<h3>服务器端5</h3>
<p>本题思路如下：</p>
<p>v<br/>
<img alt="assets/2026PolarEDF夏季赛/file-20260607135728048.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224038-1093496181.png"/></p>
<h3>服务器端6</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728049.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224130-404675307.png"/></p>
<h3>服务器端7</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728050.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224197-1491847337.png"/></p>
<h3>服务器端8</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728051.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141223938-1696529577.png"/></p>
<h3>服务器端9</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728052.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224171-329530764.png"/></p>
<h3>服务器端10</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728052.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224171-329530764.png"/></p>
<h3>服务器端11</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728053.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224143-1033761343.png"/></p>
<h3>服务器端12</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728054.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224164-1164267197.png"/></p>
<h3>服务器端13</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728055.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224211-1140618591.png"/></p>
<h3>服务器端14</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728056.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141223956-1936906819.png"/></p>
<h3>服务器端15</h3>
<p>本题思路如下：</p>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728057.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224124-220330543.png"/></p>
<h3>服务器端16.</h3>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728058.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224205-1711159869.png"/></p>
<h3>服务器端17.</h3>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728059.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224171-96849950.png"/></p>
<h3>服务器端18.</h3>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728060.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224131-2089156387.png"/></p>
<h3>服务器端19.</h3>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728061.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141223807-1676169375.png"/></p>
<h3>服务器端20.</h3>
<p><img alt="assets/2026PolarEDF夏季赛/file-20260607135728062.png" src="/assets/2026PolarEDF夏季赛wp/3539156-20260607141224187-1175288878.png"/></p>
