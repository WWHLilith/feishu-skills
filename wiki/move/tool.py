"""飞书知识库 — 将云文档移动到知识库指定目录下。"""
import argparse
import re
import sys
from pathlib import Path

_FEISHU_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_FEISHU_ROOT))

from scripts.api import api_request

# URL 中的文档类型路径 → obj_type 映射
_URL_TYPE_MAP = {
    "docx": "docx",
    "sheets": "sheet",
    "bitable": "bitable",
    "file": "file",
    "wiki": "wiki",
}


def _parse_doc_url(url: str) -> tuple[str, str]:
    """从文档 URL 提取 token 和 obj_type。"""
    # 匹配 https://xxx.feishu.cn/docx/TOKEN 或 /sheets/TOKEN 等
    m = re.search(r"feishu\.cn/(docx|sheets|bitable|file|wiki)/(\w+)", url)
    if not m:
        raise RuntimeError(f"无法从 URL 解析文档信息: {url}")
    url_type, token = m.group(1), m.group(2)
    return token, _URL_TYPE_MAP.get(url_type, "docx")


def _parse_wiki_url(url: str) -> str:
    """从知识库 URL 提取节点 token。"""
    m = re.search(r"feishu\.cn/wiki/(\w+)", url)
    if not m:
        raise RuntimeError(f"无法从 URL 解析知识库节点: {url}")
    return m.group(1)


def _get_space_id(node_token: str) -> str:
    """通过节点 token 获取 space_id。"""
    data = api_request("GET", "/wiki/v2/spaces/get_node", params={
        "token": node_token,
    }, use_user_token=True, scopes=["wiki:wiki"])
    space_id = data.get("data", {}).get("node", {}).get("space_id", "")
    if not space_id:
        raise RuntimeError(f"无法获取节点 {node_token} 的 space_id")
    return space_id


def move_to_wiki(doc_token: str, obj_type: str, parent_token: str) -> str:
    """将云文档移动到知识库节点下。"""
    space_id = _get_space_id(parent_token)

    data = api_request("POST", f"/wiki/v2/spaces/{space_id}/nodes/move_docs_to_wiki", body={
        "parent_wiki_token": parent_token,
        "obj_type": obj_type,
        "obj_token": doc_token,
    }, use_user_token=True, scopes=["wiki:wiki"])

    # 查找新节点获取标题和链接
    list_data = api_request("GET", f"/wiki/v2/spaces/{space_id}/nodes", params={
        "parent_node_token": parent_token,
        "page_size": 50,
    }, use_user_token=True, scopes=["wiki:wiki"])

    items = list_data.get("data", {}).get("items", [])
    for node in items:
        if node.get("obj_token") == doc_token:
            title = node.get("title", "")
            wiki_token = node.get("node_token", "")
            return f"移动成功\n标题: {title}\n链接: https://lilithgames.feishu.cn/wiki/{wiki_token}"

    return "移动成功（未能获取新节点详情）"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="飞书知识库 — 移动文档")
    doc_group = parser.add_mutually_exclusive_group(required=True)
    doc_group.add_argument("--doc-url", help="文档 URL")
    doc_group.add_argument("--doc-token", help="文档 token")
    parser.add_argument("--obj-type", default="docx",
                        choices=["docx", "sheet", "bitable", "file"],
                        help="文档类型（使用 --doc-token 时指定，默认 docx）")
    parent_group = parser.add_mutually_exclusive_group(required=True)
    parent_group.add_argument("--parent-url", help="目标知识库节点 URL")
    parent_group.add_argument("--parent-token", help="目标知识库节点 token")
    args = parser.parse_args()

    try:
        if args.doc_url:
            doc_token, obj_type = _parse_doc_url(args.doc_url)
        else:
            doc_token, obj_type = args.doc_token, args.obj_type

        if args.parent_url:
            parent_token = _parse_wiki_url(args.parent_url)
        else:
            parent_token = args.parent_token

        print(move_to_wiki(doc_token, obj_type, parent_token))
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)
