"""读取飞书群聊消息。"""
import argparse
import json
import sys
from pathlib import Path

_FEISHU_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_FEISHU_ROOT))

from scripts.api import api_request

SCOPES = ["im:message:readonly", "im:chat:readonly", "im:message.group_msg:get_as_user", "contact:user.base:readonly"]


def list_chats(query: str = "") -> list[dict]:
    """列出当前用户加入的群，支持按名称过滤。"""
    chats = []
    page_token = None
    while True:
        params = {"page_size": 100}
        if page_token:
            params["page_token"] = page_token
        data = api_request("GET", "/im/v1/chats", params=params, use_user_token=True, scopes=SCOPES)
        items = data.get("data", {}).get("items", [])
        chats.extend(items)
        has_more = data.get("data", {}).get("has_more", False)
        page_token = data.get("data", {}).get("page_token")
        if not has_more or not page_token:
            break
    if query:
        chats = [c for c in chats if query in c.get("name", "")]
    return chats


def get_messages(chat_id: str, count: int = 50, sender_id: str = "") -> list[dict]:
    """获取群消息，可按发送者过滤。"""
    params = {
        "container_id_type": "chat",
        "container_id": chat_id,
        "page_size": min(count, 50),
        "sort_type": "ByCreateTimeDesc",
    }
    data = api_request("GET", "/im/v1/messages", params=params, use_user_token=True, scopes=SCOPES)
    items = data.get("data", {}).get("items", [])
    if sender_id:
        items = [m for m in items if m.get("sender", {}).get("id") == sender_id]
    return items


def get_my_open_id() -> str:
    """获取当前用户的 open_id。"""
    data = api_request("GET", "/authen/v1/user_info", use_user_token=True, scopes=SCOPES)
    return data.get("data", {}).get("open_id", "")


def batch_get_user_names(open_ids: list[str]) -> dict[str, str]:
    """批量获取 open_id -> 名字的映射。"""
    if not open_ids:
        return {}
    try:
        params = [("user_id_type", "open_id")] + [("user_ids", oid) for oid in open_ids]
        data = api_request("GET", "/contact/v3/users/batch",
                           params=params, use_user_token=True, scopes=SCOPES)
        return {u.get("open_id", ""): u.get("name", "") for u in data.get("data", {}).get("items", [])}
    except Exception:
        return {}


def format_message(msg: dict, name_map: dict = None) -> str:
    name_map = name_map or {}
    sender = msg.get("sender", {})
    raw_id = sender.get("id", "unknown")
    sender_id = name_map.get(raw_id, raw_id)
    create_time = msg.get("create_time", "")
    if create_time:
        import datetime
        ts = int(create_time) / 1000
        dt = datetime.datetime.fromtimestamp(ts).strftime("%m-%d %H:%M")
    else:
        dt = ""

    # 从 mentions 字段构建 @_user_X -> 名字 的映射
    mention_map = {}
    for m in msg.get("mentions", []):
        key = m.get("key", "")       # "@_user_1"
        name = m.get("name", "")
        if key and name:
            mention_map[key] = name

    content_raw = msg.get("body", {}).get("content", "{}")
    try:
        content_obj = json.loads(content_raw)
        if "text" in content_obj:
            text = content_obj["text"]
        elif "content" in content_obj:
            # 富文本：展开每个 tag
            parts = []
            for line in content_obj["content"]:
                for seg in line:
                    tag = seg.get("tag", "")
                    if tag == "text":
                        parts.append(seg.get("text", ""))
                    elif tag == "at":
                        uid = seg.get("user_id", "")
                        uname = seg.get("user_name") or mention_map.get(uid, uid)
                        parts.append(f"@{uname}")
                    elif tag == "a":
                        parts.append(seg.get("href") or seg.get("text", ""))
                    elif tag == "img":
                        parts.append("[图片]")
                    elif tag == "emotion":
                        parts.append(f"[{seg.get('emoji_type', '表情')}]")
                parts.append("\n")
            text = "".join(parts).strip()
        else:
            text = content_raw
    except Exception:
        text = content_raw

    # 替换剩余 @_user_X 占位符（plain text 消息）
    for key, name in mention_map.items():
        text = text.replace(key, f"@{name}")

    return f"[{dt}] {sender_id}: {text}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="读取飞书群聊消息")
    sub = parser.add_subparsers(dest="cmd")

    # 列群
    p_list = sub.add_parser("list-chats", help="列出加入的群")
    p_list.add_argument("--query", default="", help="按群名过滤")

    # 读消息
    p_read = sub.add_parser("read", help="读取群消息")
    p_read.add_argument("--chat-id", help="群 chat_id")
    p_read.add_argument("--chat-name", help="按群名搜索（自动找 chat_id）")
    p_read.add_argument("--count", type=int, default=50, help="消息数量，默认50")
    p_read.add_argument("--mine", action="store_true", help="只看自己的发言")

    args = parser.parse_args()

    try:
        if args.cmd == "list-chats":
            chats = list_chats(args.query)
            if not chats:
                print("未找到匹配的群。")
            else:
                for c in chats:
                    print(f"{c.get('name', '未命名')} (chat_id: {c.get('chat_id', '')})")

        elif args.cmd == "read":
            chat_id = args.chat_id
            if not chat_id and args.chat_name:
                chats = list_chats(args.chat_name)
                if not chats:
                    print(f"[error] 未找到群名包含「{args.chat_name}」的群")
                    sys.exit(1)
                if len(chats) > 1:
                    print(f"找到多个匹配的群，请用 --chat-id 指定：")
                    for c in chats:
                        print(f"  {c.get('name')} (chat_id: {c.get('chat_id')})")
                    sys.exit(1)
                chat_id = chats[0]["chat_id"]
                print(f"群：{chats[0].get('name')} (chat_id: {chat_id})\n")

            sender_filter = ""
            if args.mine:
                sender_filter = get_my_open_id()

            msgs = get_messages(chat_id, args.count, sender_filter)
            if not msgs:
                print("没有找到消息。")
            else:
                unique_ids = list({m.get("sender", {}).get("id", "") for m in msgs
                                   if m.get("sender", {}).get("id_type") == "open_id"})
                name_map = batch_get_user_names(unique_ids)
                for m in reversed(msgs):
                    print(format_message(m, name_map))
        else:
            parser.print_help()

    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)
