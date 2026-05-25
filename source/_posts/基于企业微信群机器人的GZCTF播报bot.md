---
title: "基于企业微信群机器人的GZCTF播报bot"
date: 2025-05-27 09:25:00
categories:
  - "CTF Writeup"
tags:
  - "CTF"
  - "Writeup"
cnblogs_postid: "18897979"
cnblogs_url: "https://www.cnblogs.com/ljnljn/p/18897979"
---

都是用qq的，内部比赛可以用企业微信，连服务器都不需要
```python
import time
from datetime import datetime, timezone, timedelta
import requests
import logging
from rich.logging import RichHandler
from rich.status import Status

INTERVAL = 2  # 间隔时间
FORMAT = "%(message)s"
WEBHOOK_KEY = ''  # 替换实际webhook_key，就在key=之后，“https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=”
API_URL = 'http://网站或者ip/api/game/1/notices'  # 确认API地址正确（1是对应的比赛id）

TEMPLATES = {
    'Normal': ' 比赛公告\n内容: %s\n时间: %s',
    'NewChallenge': ' 新增题目\n题目名称: %s\n发布时间: %s',
    'NewHint': ' 题目提示\n题目名称: %s 有新提示\n更新时间: %s',
    'FirstBlood': ' 一血播报\n选手: %s\n攻破题目: %s\n时间: %s',
    'SecondBlood': '⚔️ 二血播报\n选手: %s\n攻破题目: %s\n时间: %s',
    'ThirdBlood': '⚡ 三血播报\n选手: %s\n攻破题目: %s\n时间: %s'
}


class WXWorkBot:
    """企业微信机器人封装类"""

    def __init__(self, webhook_key: str):
        self.webhook_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}"

    def send_markdown(self, content: str) -> bool:
        """发送Markdown格式消息"""
        payload = {
            "msgtype": "text",
            "text": {
                "content": content
            }
        }
        try:
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
            return True
        except Exception as e:
            logging.error(f"消息发送失败: {str(e)}")
            return False


def process_timestamp(ts: int) -> str:
    """处理毫秒级时间戳转换"""
    # 转换为北京时间
    utc_time = datetime.utcfromtimestamp(ts / 1000).replace(tzinfo=timezone.utc)
    beijing_time = utc_time.astimezone(timezone(timedelta(hours=8)))
    return beijing_time.strftime("%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    # 初始化日志和机器人
    logging.basicConfig(
        level=logging.INFO, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
    )
    log = logging.getLogger("rich")
    wx_bot = WXWorkBot(WEBHOOK_KEY)
    NOW_ID = 0

    try:
        # 获取初始最新ID
        response = requests.get(API_URL)
        notices = sorted(response.json(), key=lambda x: x['id'])
        NOW_ID = notices[-1]['id'] if notices else 0
        log.info(f"初始最新通知ID: {NOW_ID}")
    except Exception as e:
        log.error(f"初始化失败: {str(e)}")
        exit(1)

    status = Status('Waiting for new notice')
    status.start()

    while True:
        try:
            # 获取通知数据
            response = requests.get(API_URL)
            notices = sorted(response.json(), key=lambda x: x['id'])

            for notice in notices:
                if notice['id'] > NOW_ID:
                    try:
                        # 处理时间格式
                        timestamp = notice['time'] if isinstance(notice['time'], int) else int(notice['time'])
                        formatted_time = process_timestamp(timestamp)

                        # 处理values字段
                        values = notice['values']
                        if not isinstance(values, list):  # 确保是列表类型
                            values = [str(values)]

                        # 检查参数数量
                        required_params = TEMPLATES[notice['type']].count('%s') - 1  # 减去时间参数
                        if len(values) < required_params:
                            log.warning(f"参数不足的通知: ID={notice['id']} Type={notice['type']}")
                            continue

                        # 拼接参数（保留必要参数）
                        template_args = values[:required_params] + [formatted_time]

                        # 生成消息
                        message = TEMPLATES[notice['type']] % tuple(template_args)

                        if wx_bot.send_markdown(message):
                            NOW_ID = notice['id']
                            log.info(f"成功发送通知 ID: {notice['id']}")
                    except KeyError as e:
                        log.error(f"字段缺失: {str(e)} 通知内容: {notice}")
                    except Exception as e:
                        log.error(f"处理通知异常: {str(e)} 通知内容: {notice}")

            time.sleep(INTERVAL)

        except KeyboardInterrupt:
            log.info('程序已手动终止')
            break
        except requests.RequestException as e:
            log.error(f"API请求异常: {str(e)}")
            time.sleep(5)
        except Exception as e:
            log.error(f"未知错误: {str(e)}")
            time.sleep(5)

    status.stop()
```
效果：
用text原因是因为企业微信在微信上的捷径只能通过文字发送，所以干脆就这样了（笑
![image](/assets/cnblogs/基于企业微信群机器人的GZCTF播报bot/3539156-20250527092336527-1979337781.png)
![image](/assets/cnblogs/基于企业微信群机器人的GZCTF播报bot/3539156-20250527092358389-610096019.png)
![image](/assets/cnblogs/基于企业微信群机器人的GZCTF播报bot/3539156-20250527092417010-1252627328.png)
