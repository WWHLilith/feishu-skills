"""飞书 Webhook 消息发送。"""
import argparse
import json
import sys

import requests


def send_webhook(url: str, text: str = "", rich: str = "") -> str:
    if rich:
        body = {"msg_type": "post", "content": json.loads(rich)}
    else:
        body = {"msg_type": "text", "content": {"text": text}}

    resp = requests.post(url, json=body, timeout=10)
    data = resp.json()

    if data.get("code", 0) != 0 and data.get("StatusCode", 0) != 0:
        return f"[error] webhook 发送失败: {data.get('msg', data)}"
    return "Webhook 消息发送成功"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="飞书 Webhook 消息")
    parser.add_argument("--url", required=True, help="Webhook URL")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", help="纯文本消息")
    group.add_argument("--rich", help="富文本 JSON")
    args = parser.parse_args()
    try:
        print(send_webhook(args.url, text=args.text or "", rich=args.rich or ""))
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)
