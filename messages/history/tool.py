"""飞书聊天记录读取 — 获取与指定用户的对话历史。"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

_FEISHU_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_FEISHU_ROOT))

from scripts.api import api_request


def _search_user(name: str) -> str:
    """按名称搜索用户，返回 open_id。"""
    data = api_request("GET", "/search/v1/user", params={"query": name, "page_size": 5},
                       use_user_token=True, scopes=["contact:user:search"])
    users = data.get("data", {}).get("users", [])
    if not users:
        raise RuntimeError(f"未找到匹配 \"{name}\" 的用户")
    # 优先精确匹配
    for u in users:
        if u.get("name") == name:
            return u["open_id"]
    return users[0]["open_id"]


def _get_p2p_chat_id(open_id: str) -> str:
    """通过发送临时消息获取与指定用户的单聊 chat_id，然后删除该消息。

    飞书 API 不支持直接列出单聊会话，官方推荐的获取单聊 chat_id 的方式
    是通过发送消息接口，从响应中获取 chat_id。
    """
    # 发送通知消息，同时从响应中获取 chat_id
    notice = f"[Claude Agent 正在获取会话内容]"
    data = api_request("POST", "/im/v1/messages", params={
        "receive_id_type": "open_id",
    }, body={
        "receive_id": open_id,
        "msg_type": "text",
        "content": json.dumps({"text": notice}),
    }, use_user_token=True, scopes=["im:message", "im:message:readonly"])

    msg_data = data.get("data", {})
    chat_id = msg_data.get("chat_id", "")

    if not chat_id:
        raise RuntimeError("发送通知消息后未获取到 chat_id")

    return chat_id


def _extract_text(msg: dict) -> str:
    """从消息体提取可读文本。"""
    msg_type = msg.get("msg_type", "")
    body = msg.get("body", {})
    content_str = body.get("content", "{}")

    try:
        content = json.loads(content_str)
    except (json.JSONDecodeError, TypeError):
        return content_str or "[无法解析]"

    if msg_type == "text":
        return content.get("text", "")
    elif msg_type == "post":
        # 富文本：提取所有文本段
        lines = []
        for lang in ("zh_cn", "en_us"):
            post = content.get(lang)
            if post:
                title = post.get("title", "")
                if title:
                    lines.append(title)
                for para in post.get("content", []):
                    parts = []
                    for elem in para:
                        if elem.get("tag") == "text":
                            parts.append(elem.get("text", ""))
                        elif elem.get("tag") == "a":
                            parts.append(elem.get("text", "") or elem.get("href", ""))
                        elif elem.get("tag") == "at":
                            parts.append(f"@{elem.get('user_name', elem.get('user_id', ''))}")
                    lines.append("".join(parts))
                break
        return "\n".join(lines) if lines else "[富文本]"
    elif msg_type == "image":
        return "[图片]"
    elif msg_type == "file":
        return f"[文件: {content.get('file_name', '')}]"
    elif msg_type == "sticker":
        return "[表情]"
    elif msg_type == "audio":
        return "[语音]"
    elif msg_type == "video":
        return "[视频]"
    elif msg_type == "interactive":
        title = content.get("header", {}).get("title", {}).get("content", "")
        return f"[卡片: {title}]" if title else "[卡片消息]"
    elif msg_type == "merge_forward":
        return "[合并转发]"
    elif msg_type == "system":
        return "[系统消息]"
    else:
        return f"[{msg_type}]"


def read_history(chat_id: str, limit: int = 50) -> str:
    """读取指定会话的消息历史。"""
    params = {
        "container_id_type": "chat",
        "container_id": chat_id,
        "page_size": min(limit, 50),
        "sort_type": "ByCreateTimeDesc",
    }
    data = api_request("GET", "/im/v1/messages", params=params,
                       use_user_token=True, scopes=["im:message:readonly"])
    items = data.get("data", {}).get("items", [])
    if not items:
        return "该会话暂无消息。"

    # 按时间正序显示（API 返回倒序）
    items.reverse()

    lines = []
    for msg in items:
        sender = msg.get("sender", {})
        sender_type = sender.get("sender_type", "")
        sender_id = sender.get("id", "")
        create_time = msg.get("create_time", "")

        # 格式化时间
        time_str = ""
        if create_time:
            try:
                ts = int(create_time) / 1000
                time_str = datetime.fromtimestamp(ts).strftime("%m-%d %H:%M")
            except (ValueError, OSError):
                time_str = create_time

        text = _extract_text(msg)
        sender_label = f"[{sender_type}:{sender_id[:8]}...]" if sender_id else "[未知]"
        lines.append(f"[{time_str}] {sender_label}: {text}")

    return "\n".join(lines)


def read_history_by_name(name: str, limit: int = 50) -> str:
    """按用户名搜索并读取单聊对话历史。

    流程：搜索用户 → 发临时消息获取 chat_id → 删除临时消息 → 读取历史。
    """
    open_id = _search_user(name)
    chat_id = _get_p2p_chat_id(open_id)
    return read_history(chat_id, limit)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="飞书聊天记录读取")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--name", help="对方用户名（自动搜索用户并查找单聊）")
    group.add_argument("--chat-id", help="直接指定 chat_id")
    parser.add_argument("--limit", type=int, default=50, help="获取消息条数（默认 50）")
    args = parser.parse_args()
    try:
        if args.name:
            print(read_history_by_name(args.name, args.limit))
        else:
            print(read_history(args.chat_id, args.limit))
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)
