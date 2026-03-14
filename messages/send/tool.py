"""飞书发送消息。"""
import argparse
import json
import sys
from pathlib import Path

_FEISHU_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_FEISHU_ROOT))

from scripts.api import api_request


def send_message(receive_id: str, receive_id_type: str, text: str = "", rich: str = "", card: str = "") -> str:
    if card:
        msg_type = "interactive"
        content = card
    elif rich:
        msg_type = "post"
        content = rich
    else:
        msg_type = "text"
        content = json.dumps({"text": text})

    data = api_request("POST", "/im/v1/messages", params={
        "receive_id_type": receive_id_type,
    }, body={
        "receive_id": receive_id,
        "msg_type": msg_type,
        "content": content,
    }, use_user_token=False)  # 消息以机器人身份发送
    msg_id = data.get("data", {}).get("message_id", "")
    return f"消息发送成功 (message_id: {msg_id})"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="飞书发送消息")
    parser.add_argument("--to", required=True, help="接收方 ID")
    parser.add_argument("--type", required=True, choices=["open_id", "user_id", "email", "chat_id"], help="ID 类型")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", help="纯文本消息")
    group.add_argument("--rich", help="富文本 JSON")
    group.add_argument("--card", help="卡片消息 JSON")
    args = parser.parse_args()
    try:
        print(send_message(args.to, args.type, text=args.text or "", rich=args.rich or "", card=args.card or ""))
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)
