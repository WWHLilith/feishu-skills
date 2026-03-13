"""飞书通讯录查询。"""
import argparse
import sys
from pathlib import Path

_FEISHU_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_FEISHU_ROOT))

from scripts.api import api_request


def search_user(query: str) -> str:
    data = api_request("POST", "/search/v1/user", params={"query": query, "page_size": 10},
                       body={"query": query}, use_user_token=True)
    users = data.get("data", {}).get("users", [])
    if not users:
        return f"未找到匹配 \"{query}\" 的用户。"
    lines = []
    for i, u in enumerate(users, 1):
        name = u.get("name", "N/A")
        open_id = u.get("open_id", "")
        dept = ", ".join(u.get("department_names", [])) or "未知部门"
        lines.append(f"{i}. {name} (open_id: {open_id}, 部门: {dept})")
    return "\n".join(lines)


def get_user(user_id: str) -> str:
    data = api_request("GET", f"/contact/v3/users/{user_id}", params={
        "user_id_type": "open_id"
    })
    u = data.get("data", {}).get("user", {})
    if not u:
        return f"[error] 未找到用户: {user_id}"
    name = u.get("name", "N/A")
    email = u.get("email", "N/A")
    mobile = u.get("mobile", "N/A")
    status = u.get("status", {})
    active = "活跃" if status.get("is_activated") else "未激活"
    return f"姓名: {name}\nOpen ID: {user_id}\n邮箱: {email}\n手机: {mobile}\n状态: {active}"


def get_user_by_email(email: str) -> str:
    data = api_request("POST", "/contact/v3/users/batch_get_id", body={
        "emails": [email],
    }, params={"user_id_type": "open_id"})
    users = data.get("data", {}).get("user_list", [])
    if not users or not users[0].get("user_id"):
        return f"未找到邮箱 {email} 对应的用户。"
    user_id = users[0]["user_id"]
    return get_user(user_id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="飞书通讯录查询")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--search", help="按名称搜索用户")
    group.add_argument("--user-id", help="按 open_id 获取用户信息")
    group.add_argument("--email", help="按邮箱查询用户")
    args = parser.parse_args()
    try:
        if args.search:
            print(search_user(args.search))
        elif args.user_id:
            print(get_user(args.user_id))
        else:
            print(get_user_by_email(args.email))
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)
