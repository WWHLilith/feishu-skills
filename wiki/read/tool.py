"""飞书知识库页面阅读。"""
import argparse
import re
import sys
from pathlib import Path

_FEISHU_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_FEISHU_ROOT))

from scripts.api import api_request


def _parse_wiki_url(url: str) -> str:
    m = re.search(r"feishu\.cn/wiki/([A-Za-z0-9]+)", url)
    return m.group(1) if m else url


def read_wiki(token: str) -> str:
    # 解析 wiki token → docx token
    node = api_request("GET", "/wiki/v2/spaces/get_node", params={"token": token}, scopes=["wiki:wiki"])
    node_data = node.get("data", {}).get("node", {})
    obj_token = node_data.get("obj_token", "")
    title = node_data.get("title", "N/A")

    if not obj_token:
        return f"[error] 无法解析 wiki token: {token}"

    # 读取文档内容
    content = api_request("GET", f"/docx/v1/documents/{obj_token}/raw_content", scopes=["docx:document"])
    raw = content.get("data", {}).get("content", "")
    return f"标题: {title}\n---\n{raw if raw else '(内容为空)'}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="阅读飞书知识库页面")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--token", help="知识库节点 token")
    group.add_argument("--url", help="飞书知识库页面 URL")
    args = parser.parse_args()
    try:
        t = args.token or _parse_wiki_url(args.url)
        print(read_wiki(t))
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)
