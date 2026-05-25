---
title: "ropper启动失败的解决方案"
date: 2025-01-14 14:54:00
categories:
  - "CTF Writeup"
tags:
  - "CTF"
  - "Writeup"
  - "Pwn"
cnblogs_postid: "18670772"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18670772"
---

用ropper做题报错
```
Traceback (most recent call last):
  File "/usr/bin/ropper", line 33, in <module>
    sys.exit(load_entry_point('ropper==1.13.8', 'console_scripts', 'ropper')())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/bin/ropper", line 25, in importlib_load_entry_point
    return next(matches).load()
           ^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/importlib/metadata/__init__.py", line 205, in load
    module = import_module(match.group('module'))
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/importlib/__init__.py", line 90, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1310, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 995, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/usr/lib/python3/dist-packages/ropper/__init__.py", line 29, in <module>
    from .console import Console
  File "/usr/lib/python3/dist-packages/ropper/console.py", line 29, in <module>
    from ropper.loaders.loader import Loader, Type
  File "/usr/lib/python3/dist-packages/ropper/loaders/__init__.py", line 29, in <module>
    from . import elf
  File "/usr/lib/python3/dist-packages/ropper/loaders/elf.py", line 30, in <module>
    from ropper.loaders.loader import *
  File "/usr/lib/python3/dist-packages/ropper/loaders/loader.py", line 33, in <module>
    from ropper.arch import *
  File "/usr/lib/python3/dist-packages/ropper/arch.py", line 535, in <module>
    ARM64 = ArchitectureArm64()
            ^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/ropper/common/abstract.py", line 41, in __call__
    self._instance = super(AbstractSingletonMeta, self).__call__()
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/ropper/arch.py", line 441, in __init__
    super(ArchitectureArm64, self).__init__(CS_ARCH_ARM64, CS_MODE_ARM, 8, 4)
                                            ^^^^^^^^^^^^^
NameError: name 'CS_ARCH_ARM64' is not defined. Did you mean: 'CS_ARCH_ARM'?
```
看了github后得知目前ropper没有更新，所以要用旧版capstone
```
pip3 install capstone==5.0.1
```
运行后再启动ropper正常运行
（为什么是5.0.1：ROPgadget要求ropper版本在5.0.1以上，这个版本两个程序都能运行）
