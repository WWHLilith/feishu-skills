"""飞书知识库搜索。"""
import argparse
import sys
from pathlib import Path

_FEISHU_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_FEISHU_ROOT))

from scripts.api import api_request


def search_wiki(query: str, space_id: str = "", count: int = 10) -> str:
    """搜索知识库。指定 space_id 时遍历该空间的一级节点；否则遍历所有空间的一级节点。"""
    if space_id:
        spaces = [{"space_id": space_id, "name": ""}]
    else:
        resp = api_request("GET", "/wiki/v2/spaces", params={"page_size": 50},
                           use_user_token=True, scopes=["wiki:wiki"])
        spaces = resp.get("data", {}).get("items", [])
        if not spaces:
            return "未找到任何知识空间。"

    results = []
    for space in spaces:
        sid = space.get("space_id", "")
        sname = space.get("name", "")
        page_token = ""
        while True:
            params = {"page_size": 50}
            if page_token:
                params["page_token"] = page_token
            try:
                resp = api_request("GET", f"/wiki/v2/spaces/{sid}/nodes", params=params,
                                   use_user_token=True, scopes=["wiki:wiki"])
            except Exception:
                break
            nodes = resp.get("data", {}).get("items", [])
            for node in nodes:
                title = node.get("title", "")
                if query.lower() in title.lower():
                    results.append({
                        "title": title,
                        "token": node.get("node_token", ""),
                        "space_name": sname,
                    })
            if not resp.get("data", {}).get("has_more"):
                break
            page_token = resp.get("data", {}).get("page_token", "")
            if not page_token:
                break
        if len(results) >= count:
            break

    if not results:
        return f"未找到包含 \"{query}\" 的知识库页面。（仅搜索了各空间一级节点，深层页面需提供 space_id）"

    lines = []
    for i, r in enumerate(results[:count], 1):
        lines.append(f"{i}. {r['title']} (token: {r['token']}, 空间: {r['space_name']})")
    return "\n".join(lines)


def browse_node(parent_token: str) -> str:
    """浏览指定节点的子节点列表。"""
    # 先获取父节点信息
    try:
        parent = api_request("GET", "/wiki/v2/spaces/get_node", params={"token": parent_token},
                             use_user_token=True, scopes=["wiki:wiki"])
        parent_data = parent.get("data", {}).get("node", {})
        space_id = parent_data.get("space_id", "")
        parent_title = parent_data.get("title", parent_token)
    except Exception:
        space_id = ""
        parent_title = parent_token

    # 获取子节点
    params = {"page_size": 50, "parent_node_token": parent_token}
    try:
        resp = api_request("GET", f"/wiki/v2/spaces/{space_id}/nodes", params=params,
                           use_user_token=True, scopes=["wiki:wiki"])
    except Exception as e:
        return f"[error] {e}"

    nodes = resp.get("data", {}).get("items", [])
    if not nodes:
        return f"\"{parent_title}\" 下没有子节点。"

    lines = [f"\"{parent_title}\" 的子节点 (共 {len(nodes)} 个):"]
    for i, node in enumerate(nodes, 1):
        title = node.get("title", "N/A")
        token = node.get("node_token", "")
        has_child = "📁" if node.get("has_child") else "📄"
        lines.append(f"{i}. {has_child} {title} (token: {token})")
    return "\n".join(lines)


def list_spaces() -> str:
    resp = api_request("GET", "/wiki/v2/spaces", params={"page_size": 50},
                       use_user_token=True, scopes=["wiki:wiki"])
    spaces = resp.get("data", {}).get("items", [])
    if not spaces:
        return "未找到任何知识空间。"
    lines = [f"共 {len(spaces)} 个知识空间:"]
    for i, s in enumerate(spaces, 1):
        lines.append(f"{i}. {s.get('name', 'N/A')} (space_id: {s.get('space_id', '')})")
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="搜索飞书知识库")
    parser.add_argument("--query", default="", help="搜索关键词")
    parser.add_argument("--space-id", default="", help="知识空间 ID")
    parser.add_argument("--count", type=int, default=10, help="返回数量")
    parser.add_argument("--list-spaces", action="store_true", help="列出所有知识空间")
    parser.add_argument("--browse", default="", help="浏览指定节点的子节点")
    args = parser.parse_args()
    try:
        if args.list_spaces:
            print(list_spaces())
        elif args.browse:
            print(browse_node(args.browse))
        elif args.query:
            print(search_wiki(args.query, args.space_id, args.count))
        else:
            print("[error] 需要 --query、--list-spaces 或 --browse", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)
