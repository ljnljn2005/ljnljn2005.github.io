---
title: "DIDCTF 应急响应 流量+日志分析+数据恢复部分"
date: 2026-05-06 20:58:00
categories:
  - "Forensics Writeup"
tags:
  - "Forensics"
  - "Writeup"
  - "DIDCTF"
cnblogs_postid: "19982779"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/19982779"
---

[DIDCTF-电子数据取证综合平台](https://forensics.didctf.com/practice/questions)
## linux-basic-command
网站日志分析
用goaccess工具
![assets/DIDCTF 应急响应 流量日志分析部分/file-20260505175415310.png](/assets/cnblogs/DIDCTF 应急响应 流量+日志分析+数据恢复部分/3539156-20260506205738261-2035872319.png)

## ire7-windows-log
筛选一下就出来了
![assets/DIDCTF 应急响应 流量日志分析部分/file-20260506204153128.png](/assets/cnblogs/DIDCTF 应急响应 流量+日志分析+数据恢复部分/3539156-20260506205738336-2130354532.png)
## wireshark0
telnet流量
![assets/DIDCTF 应急响应 流量日志分析部分/file-20260506183552210.png](/assets/cnblogs/DIDCTF 应急响应 流量+日志分析+数据恢复部分/3539156-20260506205738165-2113916017.png)
## wireshark0.5
`http.request.method=="POST"`找login位置
![assets/DIDCTF 应急响应 流量日志分析部分/file-20260506185330908.png](/assets/cnblogs/DIDCTF 应急响应 流量+日志分析+数据恢复部分/3539156-20260506205738271-1937991166.png)
## wireshark1
最后一个post流执行了压缩命令，密码是Adm1n!
![assets/DIDCTF 应急响应 流量日志分析部分/file-20260506192150964.png](/assets/cnblogs/DIDCTF 应急响应 流量+日志分析+数据恢复部分/3539156-20260506205738227-1381129604.png)
另外我们可以分离出下载的压缩包
![assets/DIDCTF 应急响应 流量日志分析部分/file-20260506192212288.png](/assets/cnblogs/DIDCTF 应急响应 流量+日志分析+数据恢复部分/3539156-20260506205738270-525812706.png)
打开文件就可以获得key
![assets/DIDCTF 应急响应 流量日志分析部分/file-20260506192230824.png](/assets/cnblogs/DIDCTF 应急响应 流量+日志分析+数据恢复部分/3539156-20260506205738051-2067300805.png)
## wireshark2
让ai写了个icmp解析器
```
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import re
from datetime import datetime

try:
    from scapy.all import rdpcap, IP, IPv6, ICMP, ICMPv6EchoRequest, ICMPv6EchoReply, Raw
except ImportError:
    messagebox.showerror("缺少依赖", "请先安装 scapy：pip install scapy")
    raise


def printable_ascii(data: bytes) -> str:
    return ''.join(chr(b) if 32 <= b <= 126 else '.' for b in data)


def extract_strings(data: bytes, min_len=4):
    text = printable_ascii(data)
    return re.findall(r"[ -~]{" + str(min_len) + r",}", text)


def hex_dump(data: bytes, width=16):
    lines = []
    for i in range(0, len(data), width):
        chunk = data[i:i + width]
        hex_part = " ".join(f"{b:02x}" for b in chunk)
        ascii_part = printable_ascii(chunk)
        lines.append(f"{i:08x}  {hex_part:<{width * 3}}  {ascii_part}")
    return "\n".join(lines)


class ICMPParserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ICMP 流量解析器")
        self.root.geometry("1200x720")

        self.packets = []
        self.icmp_records = []

        self.build_ui()

    def build_ui(self):
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=8, pady=6)

        ttk.Button(top_frame, text="打开 PCAP/PCAPNG", command=self.open_file).pack(side=tk.LEFT, padx=4)
        ttk.Button(top_frame, text="搜索 key/flag", command=self.search_sensitive).pack(side=tk.LEFT, padx=4)
        ttk.Button(top_frame, text="提取所有可见字符串", command=self.show_all_strings).pack(side=tk.LEFT, padx=4)
        ttk.Button(top_frame, text="拼接 Echo Request 首字符", command=self.rebuild_first_chars).pack(side=tk.LEFT, padx=4)
        ttk.Button(top_frame, text="清空", command=self.clear).pack(side=tk.LEFT, padx=4)

        self.status_var = tk.StringVar(value="请打开一个流量包")
        ttk.Label(top_frame, textvariable=self.status_var).pack(side=tk.RIGHT, padx=8)

        main_pane = ttk.PanedWindow(self.root, orient=tk.VERTICAL)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)

        table_frame = ttk.Frame(main_pane)
        main_pane.add(table_frame, weight=2)

        columns = ("no", "time", "src", "dst", "proto", "type", "code", "len", "ascii")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        headers = {
            "no": "序号",
            "time": "时间",
            "src": "源地址",
            "dst": "目的地址",
            "proto": "协议",
            "type": "Type",
            "code": "Code",
            "len": "数据长度",
            "ascii": "Data ASCII 预览"
        }

        widths = {
            "no": 60,
            "time": 160,
            "src": 150,
            "dst": 150,
            "proto": 80,
            "type": 80,
            "code": 80,
            "len": 80,
            "ascii": 420
        }

        for col in columns:
            self.tree.heading(col, text=headers[col])
            self.tree.column(col, width=widths[col], anchor=tk.W)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<<TreeviewSelect>>", self.on_packet_select)

        detail_frame = ttk.Frame(main_pane)
        main_pane.add(detail_frame, weight=3)

        detail_label = ttk.Label(detail_frame, text="数据区详情：Hex + ASCII")
        detail_label.pack(anchor=tk.W)

        self.text = tk.Text(detail_frame, wrap=tk.NONE, font=("Consolas", 11))
        self.text.pack(fill=tk.BOTH, expand=True)

        x_scroll = ttk.Scrollbar(detail_frame, orient=tk.HORIZONTAL, command=self.text.xview)
        x_scroll.pack(fill=tk.X)
        self.text.configure(xscrollcommand=x_scroll.set)

    def open_file(self):
        file_path = filedialog.askopenfilename(
            title="选择流量包",
            filetypes=[
                ("PCAP files", "*.pcap *.pcapng"),
                ("All files", "*.*")
            ]
        )

        if not file_path:
            return

        try:
            self.clear()
            self.status_var.set("正在解析，请稍等...")

            self.packets = rdpcap(file_path)
            self.parse_icmp_packets()

            self.status_var.set(f"已加载：{file_path}，共发现 {len(self.icmp_records)} 个 ICMP/ICMPv6 包")

            if not self.icmp_records:
                messagebox.showinfo("提示", "没有发现 ICMP/ICMPv6 数据包")

        except Exception as e:
            messagebox.showerror("解析失败", str(e))
            self.status_var.set("解析失败")

    def parse_icmp_packets(self):
        for index, pkt in enumerate(self.packets, start=1):
            record = None

            if IP in pkt and ICMP in pkt:
                ip = pkt[IP]
                icmp = pkt[ICMP]
                payload = bytes(icmp.payload)

                record = {
                    "no": index,
                    "time": self.format_time(float(pkt.time)),
                    "src": ip.src,
                    "dst": ip.dst,
                    "proto": "ICMP",
                    "type": int(icmp.type),
                    "code": int(icmp.code),
                    "payload": payload,
                    "summary": pkt.summary()
                }

            elif IPv6 in pkt and (ICMPv6EchoRequest in pkt or ICMPv6EchoReply in pkt):
                ip = pkt[IPv6]
                if ICMPv6EchoRequest in pkt:
                    icmp6 = pkt[ICMPv6EchoRequest]
                    icmp_type = 128
                else:
                    icmp6 = pkt[ICMPv6EchoReply]
                    icmp_type = 129

                payload = bytes(icmp6.payload)

                record = {
                    "no": index,
                    "time": self.format_time(float(pkt.time)),
                    "src": ip.src,
                    "dst": ip.dst,
                    "proto": "ICMPv6",
                    "type": icmp_type,
                    "code": 0,
                    "payload": payload,
                    "summary": pkt.summary()
                }

            if record:
                self.icmp_records.append(record)
                ascii_preview = printable_ascii(record["payload"])
                if len(ascii_preview) > 80:
                    ascii_preview = ascii_preview[:80] + "..."

                self.tree.insert(
                    "",
                    tk.END,
                    iid=str(len(self.icmp_records) - 1),
                    values=(
                        record["no"],
                        record["time"],
                        record["src"],
                        record["dst"],
                        record["proto"],
                        record["type"],
                        record["code"],
                        len(record["payload"]),
                        ascii_preview
                    )
                )

    def on_packet_select(self, event=None):
        selected = self.tree.selection()
        if not selected:
            return

        idx = int(selected[0])
        record = self.icmp_records[idx]
        payload = record["payload"]

        self.text.delete("1.0", tk.END)

        info = []
        info.append(f"原始包序号：{record['no']}")
        info.append(f"时间：{record['time']}")
        info.append(f"源地址：{record['src']}")
        info.append(f"目的地址：{record['dst']}")
        info.append(f"协议：{record['proto']}")
        info.append(f"Type/Code：{record['type']}/{record['code']}")
        info.append(f"Payload 长度：{len(payload)} 字节")
        info.append(f"摘要：{record['summary']}")
        info.append("")
        info.append("ASCII：")
        info.append(printable_ascii(payload))
        info.append("")
        info.append("Hex Dump：")
        info.append(hex_dump(payload))

        self.text.insert(tk.END, "\n".join(info))

    def search_sensitive(self):
        if not self.icmp_records:
            messagebox.showinfo("提示", "请先打开流量包")
            return

        keywords = ["key", "flag", "password", "pass", "secret", "token"]
        result = []

        for record in self.icmp_records:
            data = printable_ascii(record["payload"])
            lower_data = data.lower()

            if any(k in lower_data for k in keywords):
                result.append(
                    f"[包序号 {record['no']}] {record['src']} -> {record['dst']} "
                    f"Type={record['type']} Code={record['code']}\n{data}\n"
                )

        self.text.delete("1.0", tk.END)

        if result:
            self.text.insert(tk.END, "发现疑似敏感内容：\n\n")
            self.text.insert(tk.END, "\n".join(result))
        else:
            self.text.insert(tk.END, "没有直接发现 key/flag/password/secret/token 等关键字。\n")
            self.text.insert(tk.END, "可以尝试点击“提取所有可见字符串”继续查看。")

    def show_all_strings(self):
        if not self.icmp_records:
            messagebox.showinfo("提示", "请先打开流量包")
            return

        result = []

        for record in self.icmp_records:
            strings = extract_strings(record["payload"], min_len=4)
            if strings:
                result.append(f"[包序号 {record['no']}] {record['src']} -> {record['dst']}")
                for s in strings:
                    result.append(f"  {s}")
                result.append("")

        self.text.delete("1.0", tk.END)

        if result:
            self.text.insert(tk.END, "\n".join(result))
        else:
            self.text.insert(tk.END, "没有提取到长度 >= 4 的可见字符串。")

    def rebuild_first_chars(self):
        if not self.icmp_records:
            messagebox.showinfo("提示", "请先打开流量包")
            return

        chars_all = []
        chars_request = []

        for record in self.icmp_records:
            payload = record["payload"]
            if not payload:
                continue

            first_char = chr(payload[0]) if 32 <= payload[0] <= 126 else "."
            chars_all.append(first_char)

            if record["proto"] == "ICMP" and record["type"] == 8:
                chars_request.append(first_char)

            if record["proto"] == "ICMPv6" and record["type"] == 128:
                chars_request.append(first_char)

        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, "所有 ICMP/ICMPv6 Payload 首字符拼接：\n")
        self.text.insert(tk.END, "".join(chars_all))
        self.text.insert(tk.END, "\n\nEcho Request Payload 首字符拼接：\n")
        self.text.insert(tk.END, "".join(chars_request))

    def clear(self):
        self.packets = []
        self.icmp_records = []
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.text.delete("1.0", tk.END)
        self.status_var.set("已清空")

    @staticmethod
    def format_time(ts):
        try:
            return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            return str(ts)


if __name__ == "__main__":
    root = tk.Tk()
    app = ICMPParserApp(root)
    root.mainloop()
```
![assets/DIDCTF 应急响应 流量日志分析部分/file-20260506202546489.png](/assets/cnblogs/DIDCTF 应急响应 流量+日志分析+数据恢复部分/3539156-20260506205738514-73492687.png)
一共执行三次命令，第三次就显示key1了
## wireshark2.1
分离
![assets/DIDCTF 应急响应 流量日志分析部分/file-20260506203140571.png](/assets/cnblogs/DIDCTF 应急响应 流量+日志分析+数据恢复部分/3539156-20260506205738368-590009101.png)
题目告诉了解压密码直接用就行
![assets/DIDCTF 应急响应 流量日志分析部分/file-20260506203157369.png](/assets/cnblogs/DIDCTF 应急响应 流量+日志分析+数据恢复部分/3539156-20260506205738228-1629178566.png)
## wireshark3
这里发现一个key
![assets/DIDCTF 应急响应 流量日志分析部分/file-20260506203547084.png](/assets/cnblogs/DIDCTF 应急响应 流量+日志分析+数据恢复部分/3539156-20260506205738363-1617255856.png)
并且提取的压缩包中有一个带密码，拿这个解
![assets/DIDCTF 应急响应 流量日志分析部分/file-20260506203613424.png](/assets/cnblogs/DIDCTF 应急响应 流量+日志分析+数据恢复部分/3539156-20260506205738151-1342385891.png)
后面大家都知道了
## linux-log
找第一次accepted password的位置
![assets/DIDCTF 应急响应 流量日志分析部分/file-20260506204822237.png](/assets/cnblogs/DIDCTF 应急响应 流量+日志分析+数据恢复部分/3539156-20260506205738301-480829471.png)
## welog1
只有最后三条是200
![assets/DIDCTF 应急响应 流量日志分析部分/file-20260506205002488.png](/assets/cnblogs/DIDCTF 应急响应 流量+日志分析+数据恢复部分/3539156-20260506205738380-1040898581.png)
![assets/DIDCTF 应急响应 流量日志分析部分/file-20260506205105016.png](/assets/cnblogs/DIDCTF 应急响应 流量+日志分析+数据恢复部分/3539156-20260506205738256-666905731.png)
发现有一串hex可疑，进行单独解码
![assets/DIDCTF 应急响应 流量日志分析部分/file-20260506205118682.png](/assets/cnblogs/DIDCTF 应急响应 流量+日志分析+数据恢复部分/3539156-20260506205738282-958988056.png)
获得了连接密码
## data-recovery
用ufs恢复，发现flag
![assets/DIDCTF 应急响应 流量日志分析部分/file-20260506205459094.png](/assets/cnblogs/DIDCTF 应急响应 流量+日志分析+数据恢复部分/3539156-20260506205738540-1237282538.png)
打开就看得到
![assets/DIDCTF 应急响应 流量日志分析部分/file-20260506205610675.png](/assets/cnblogs/DIDCTF 应急响应 流量+日志分析+数据恢复部分/3539156-20260506205738285-1849613072.png)
