"""飞书文档搜索。"""
import argparse
import sys
from pathlib import Path

_FEISHU_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_FEISHU_ROOT))

from scripts.api import api_request


def search_docs(query: str, count: int = 10) -> str:
    # 优先使用新版搜索 API
    try:
        data = api_request("POST", "/search/v1/suite/doc", body={
            "query": query,
            "page_size": count,
        }, use_user_token=True)
        items = data.get("data", {}).get("items", [])
        if items:
            lines = []
            for i, item in enumerate(items, 1):
                title = item.get("title", "N/A")
                url = item.get("url", "")
                doc_type = item.get("type", "")
                token = item.get("doc_token", "") or item.get("obj_token", "")
                lines.append(f"{i}. {title} (ID: {token}, 类型: {doc_type}, 链接: {url})")
            return "\n".join(lines)
    except Exception:
        pass

    # 回退到旧版 API
    data = api_request("POST", "/suite/docs-api/search/object", body={
        "search_key": query,
        "count": count,
        "docs_types": [2, 8, 11, 12, 15, 16],
    }, use_user_token=True)
    items = data.get("data", {}).get("docs_entities", [])
    if not items:
        return "未找到匹配的文档。"
    lines = []
    for i, item in enumerate(items, 1):
        token = item.get("docs_token", "")
        doc_type = item.get("docs_type", "")
        url = item.get("url", "")
        title = item.get("title", "N/A")
        lines.append(f"{i}. {title} (ID: {token}, 类型: {doc_type}, 链接: {url})")
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="搜索飞书文档")
    parser.add_argument("--query", required=True, help="搜索关键词")
    parser.add_argument("--count", type=int, default=10, help="返回数量")
    args = parser.parse_args()
    try:
        print(search_docs(args.query, args.count))
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)
