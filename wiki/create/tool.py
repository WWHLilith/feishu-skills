"""飞书知识库 — 在指定页面下创建子页面。"""
import argparse
import re
import sys
from pathlib import Path

_FEISHU_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_FEISHU_ROOT))

from scripts.api import api_request


def _parse_wiki_token(url_or_token: str) -> str:
    m = re.search(r"feishu\.cn/wiki/([A-Za-z0-9]+)", url_or_token)
    return m.group(1) if m else url_or_token


def get_space_id(node_token: str) -> str:
    node = api_request("GET", "/wiki/v2/spaces/get_node", params={"token": node_token}, scopes=["wiki:wiki"])
    space_id = node.get("data", {}).get("node", {}).get("space_id", "")
    if not space_id:
        raise RuntimeError(f"无法获取 space_id，node_token={node_token}")
    return space_id


def create_wiki_page(parent_token: str, title: str) -> dict:
    space_id = get_space_id(parent_token)
    body = {
        "obj_type": "doc",
        "parent_node_token": parent_token,
        "node_type": "origin",
        "title": title,
    }
    result = api_request("POST", f"/wiki/v2/spaces/{space_id}/nodes", body=body, scopes=["wiki:wiki"])
    node = result.get("data", {}).get("node", {})
    return node


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="在飞书知识库指定页面下创建子页面")
    parser.add_argument("--parent", required=True, help="父页面的 token 或完整 URL")
    parser.add_argument("--title", required=True, help="新页面标题")
    args = parser.parse_args()

    try:
        parent_token = _parse_wiki_token(args.parent)
        node = create_wiki_page(parent_token, args.title)
        wiki_token = node.get("node_token", "")
        url = f"https://lilithgames.feishu.cn/wiki/{wiki_token}" if wiki_token else "(未知)"
        print(f"创建成功")
        print(f"标题: {node.get('title', args.title)}")
        print(f"Token: {wiki_token}")
        print(f"URL: {url}")
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)
