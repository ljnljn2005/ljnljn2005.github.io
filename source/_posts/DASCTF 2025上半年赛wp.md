---
title: "DASCTF 2025上半年赛wp"
date: 2025-06-22 17:07:00
categories:
  - "CTF Writeup"
tags:
  - "CTF"
  - "Writeup"
  - "DASCTF"
cnblogs_postid: "18942899"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18942899"
---

isaxdx 28名
## Excessive Security
先找到x1、x2
```python
from Crypto.Util.number import inverse

# Given values
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

h1 = 68926494835039378729440404424793589316085902585443402029912033361291851069895
s1 = 70264613994433317101824708333691569351293428290775945022557096997867421112623
r1 = 95467825458659408375936425122753380788640181504557006906236884175684680903422

h2 = 99816429822339421445908151468618514820067970997726274244928092260385418279182
s2 = 27386247988345867998752358066350183725137348277248603318763377237810993039608
# r1 same as above

h3 = 100471089356874379799029324099340355602511511524623953182021635156113287196537
s3 = 108271537842404710192407976239166854351892165018292127464175836717873395489565
r2 = 13940715298251935708383205669373172931583958487449924842542107474174521484127

h4 = 53552261622392134420510144174810499568173979993026285111445672642139328877380
s4 = 100312693542625967610858608130705401648902828203826044299984002070083890684220
# r2 same as above

# Compute inverses
inv_s1 = inverse(s1, n)
inv_s2 = inverse(s2, n)
inv_s3 = inverse(s3, n)
inv_s4 = inverse(s4, n)

# Compute A, B, C, D, E, F
A = (r1 * inv_s2) % n
B = (r1 * inv_s1) % n
C = (h1 * inv_s1 - h2 * inv_s2) % n
D = (r2 * inv_s4) % n
E = (r2 * inv_s3) % n
F = (h3 * inv_s3 - h4 * inv_s4) % n

# Solve for x1 and x2
# From equation 1: A * x2 - B * x1 ≡ C
# From equation 2: D * x2 - E * x1 ≡ F
# Let's solve equation 1 for x2: x2 ≡ (B * x1 + C) * inv_A mod n
inv_A = inverse(A, n)
# x2 ≡ (B * x1 + C) * inv_A mod n
# Substitute into equation 2:
# D * (B * x1 + C) * inv_A - E * x1 ≡ F
# => (D * B * inv_A - E) * x1 ≡ F - D * C * inv_A
coeff_x1 = (D * B * inv_A - E) % n
rhs = (F - D * C * inv_A) % n
inv_coeff = inverse(coeff_x1, n)
x1 = (rhs * inv_coeff) % n
# Now get x2
x2 = ( (B * x1 + C) * inv_A ) % n

print(f"x1 = {x1}")
print(f"x2 = {x2}")
```
然后sagemath求解
```python
from sage.all import *

N = 98472559301398326519521704898800552100670435952553618641467704945731627783624140484670366845550939866842528582954361836035593755351584272693016822204234859506655433796327589389300744153263194916217158205372375670404000164793308078231134726345672236542974067442646354084915978240909130405000905936105602786257
e = 65537
c1 = 40127670364311180283394426274113033719543797673129006844648567069726278369353910517424074073714346881895826377902772771837790964432434997986229629267700081564740160692151350365553131535789070670584548053624970689607275665921674708650254889369926426966093575171344082441699295255661725211366819524902641461331
c2 = 4958767685161688254408001463637498631434015989118088175006720150146904021732816429444998309662995333252926794359370922113211567042198257249974382506057347524044728912256607992806670035884054654064021329936092742390064660715742236775795950389452053770118911570676738879382827738088237377423216124023239179385
x1 = 17754677231116188359396131937000664637388235962309739341039576063530375612219
x2 = 79541650983569507936838949546074094434344869740141472134648391439474061318003

P.<x> = PolynomialRing(Zmod(N))
f1 = x^e - c1
f2 = (x1 * x + x2)^e - c2
# Compute gcd(f1, f2)
# In Sage, gcd for polynomials over Zmod(N) is not directly supported, so we can use Euclidean algorithm
def poly_gcd(a, b):
    while b:
        a, b = b, a % b
    return a.monic()

gcd = poly_gcd(f1, f2)
print(gcd)
# The root is m = -gcd.coefficients()[0]
m = -gcd.coefficients()[0]
print(m)
```
丢到sagemath里解出m，然后转文字获得flag
```python
from Crypto.Util.number import long_to_bytes
print(long_to_bytes(int(m)))
```
## 鱼音乐
一眼python逆向，把主程序逆向出来
```python
# uncompyle6 version 3.9.2
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.6.12 (default, Feb  9 2021, 09:19:15)
# [GCC 8.3.0]
# Embedded file name: main.py
import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from xianyu_decrypt import load_and_decrypt_xianyu

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fish Player - 鱼音乐")
        self.resize(600, 400)
        self.player = QMediaPlayer(self)
        self.open_button = QPushButton("打开 .xianyu 文件")
        self.open_button.clicked.connect(self.open_xianyu)
        self.cover_label = QLabel("专辑封面展示")
        self.cover_label.setScaledContents(True)
        self.cover_label.setFixedSize(300, 300)
        layout = QVBoxLayout()
        layout.addWidget(self.open_button)
        layout.addWidget(self.cover_label)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_xianyu(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择 .xianyu 文件", "", "Xianyu Files (*.xianyu)")
        if not file_path:
            return
        try:
            info = load_and_decrypt_xianyu(file_path)
            meta = info["meta"]
            cover_path = info["cover_path"]
            audio_path = info["audio_path"]
            if cover_path and os.path.exists(cover_path):
                pixmap = QPixmap(cover_path)
                self.cover_label.setPixmap(pixmap)
            else:
                self.cover_label.setText("无封面")
            url = QUrl.fromLocalFile(audio_path)
            self.player.setMedia(QMediaContent(url))
            self.player.play()
            name = meta.get("name", "未知")
            artist = meta.get("artist", "未知歌手")
            fl4g = meta.get("fl4g", "where_is_the_flag?")
            FLAG = meta.get("")
            QMessageBox.information(self, "音乐提示您", f"正在播放：{name}\n歌手：{artist}\nfl4g:{fl4g}\nFLAG:{FLAG}")
        except Exception as e:
            try:
                QMessageBox.critical(self, "错误", str(e))
            finally:
                e = None
                del e


def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
```
发现里面有解密部分，但是文件是pyd，懒得逆向了，直接把主程序解密部分单独出来
这里注意需要用python3.8不然会报错
```python
import os  
import sys  
import argparse  
from xianyu_decrypt import load_and_decrypt_xianyu  
  
  
def main():  
    parser = argparse.ArgumentParser(description='鱼音乐 - .xianyu 文件解密工具')  
    parser.add_argument('file', help='需要解密的 .xianyu 文件路径')  
    args = parser.parse_args()  
  
    if not os.path.exists(args.file):  
        print(f"错误：文件 '{args.file}' 不存在")  
        sys.exit(1)  
  
    try:  
        info = load_and_decrypt_xianyu(args.file)  
        meta = info["meta"]  
  
        print("\n=== 元数据信息 ===")  
        print(f"歌曲名称: {meta.get('name', '未知')}")  
        print(f"艺术家: {meta.get('artist', '未知歌手')}")  
  
        # 尝试获取可能的flag字段  
        for key in ['fl4g', 'flag', 'FLAG']:  
            if key in meta:  
                print(f"发现特殊字段 [{key}]: {meta[key]}")  
  
        # 显示其他所有元数据  
        print("\n=== 完整元数据 ===")  
        for k, v in meta.items():  
            if k not in ['name', 'artist']:  # 跳过已显示的基础字段  
                print(f"{k}: {v}")  
  
        print("\n解密成功！")  
        print(f"封面保存至: {info['cover_path']}")  
        print(f"音频保存至: {info['audio_path']}")  
  
    except Exception as e:  
        print(f"解密过程中出错: {str(e)}")  
        sys.exit(1)  
  
  
if __name__ == "__main__":  
    main()
```
![assets/DASCTF 2025上半年赛wp/file-20250621214330723.png](/assets/cnblogs/DASCTF 2025上半年赛wp/3539156-20250622170726522-1091947961.png)
