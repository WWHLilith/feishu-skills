"""飞书文档读取。"""
import argparse
import sys
from pathlib import Path

_FEISHU_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_FEISHU_ROOT))

from scripts.api import api_request


def _extract_text(content: dict) -> str:
    """从文档 block 结构中递归提取纯文本。"""
    lines = []
    blocks = content.get("document", {}).get("body", {}).get("blocks", [])
    if not blocks:
        blocks = content.get("body", {}).get("blocks", [])
    for block in blocks:
        block_type = block.get("block_type", 0)
        if block_type in (2, 3, 4, 5, 6, 7, 8, 9, 10, 11):
            para = block.get("paragraph", {}) or block.get("heading", {})
            elements = para.get("elements", [])
            text_parts = []
            for el in elements:
                text_run = el.get("text_run", {})
                if text_run:
                    text_parts.append(text_run.get("content", ""))
            if text_parts:
                prefix = "#" * (block_type - 2) + " " if block_type > 2 else ""
                lines.append(f"{prefix}{''.join(text_parts)}")
        elif block_type == 14:
            code = block.get("code", {})
            elements = code.get("elements", [])
            text_parts = [el.get("text_run", {}).get("content", "") for el in elements]
            lines.append(f"```\n{''.join(text_parts)}\n```")
    return "\n".join(lines)


def _resolve_wiki_token(wiki_token: str) -> tuple[str, str]:
    node = api_request("GET", "/wiki/v2/spaces/get_node", params={"token": wiki_token}, scopes=["wiki:wiki"])
    node_data = node.get("data", {}).get("node", {})
    return node_data.get("obj_token", ""), node_data.get("title", "N/A")


def _parse_feishu_url(url: str) -> tuple[str, str]:
    import re
    m = re.search(r"feishu\.cn/(wiki|docx|doc)/([A-Za-z0-9]+)", url)
    if m:
        return m.group(2), m.group(1)
    return url, "docx"


def read_document(doc_id: str = "", wiki_token: str = "", url: str = "") -> str:
    if url:
        token, doc_type = _parse_feishu_url(url)
        if doc_type == "wiki":
            wiki_token = token
        else:
            doc_id = token

    if wiki_token:
        doc_id, wiki_title = _resolve_wiki_token(wiki_token)
        if not doc_id:
            return f"[error] 无法解析 wiki token: {wiki_token}"

    if not doc_id:
        return "[error] 需要提供 --doc-id、--wiki-token 或 --url 参数"

    meta = api_request("GET", f"/docx/v1/documents/{doc_id}", scopes=["docx:document"])
    title = meta.get("data", {}).get("document", {}).get("title", "N/A")

    content = api_request("GET", f"/docx/v1/documents/{doc_id}/raw_content", scopes=["docx:document"])
    raw = content.get("data", {}).get("content", "")
    if raw:
        return f"标题: {title}\n---\n{raw}"

    blocks = api_request("GET", f"/docx/v1/documents/{doc_id}/blocks", scopes=["docx:document"])
    text = _extract_text(blocks.get("data", {}))
    return f"标题: {title}\n---\n{text if text else '(文档内容为空或无法解析)'}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="读取飞书文档")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--doc-id", help="文档 ID（docx token）")
    group.add_argument("--wiki-token", help="知识库页面 token")
    group.add_argument("--url", help="飞书文档/知识库 URL")
    args = parser.parse_args()
    try:
        print(read_document(doc_id=args.doc_id or "", wiki_token=args.wiki_token or "", url=args.url or ""))
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)
