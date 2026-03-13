"""飞书文档更新（追加内容）。"""
import argparse
import sys
from pathlib import Path

_FEISHU_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_FEISHU_ROOT))

from scripts.api import api_request


def update_document(doc_id: str, content: str) -> str:
    # 获取文档的 document block ID
    blocks_data = api_request("GET", f"/docx/v1/documents/{doc_id}/blocks")
    items = blocks_data.get("data", {}).get("items", [])
    if not items:
        raise RuntimeError("无法获取文档 block 结构")

    doc_block_id = items[0].get("block_id", doc_id)

    # 按换行拆分为多个段落 block
    paragraphs = content.split("\n")
    children = []
    for para in paragraphs:
        if not para.strip():
            continue  # 跳过空行
        children.append({
            "block_type": 2,
            "text": {
                "elements": [{
                    "text_run": {"content": para, "text_element_style": {}}
                }],
                "style": {}
            }
        })

    api_request("POST", f"/docx/v1/documents/{doc_id}/blocks/{doc_block_id}/children", body={
        "children": children,
    })

    return f"文档更新成功\nID: {doc_id}\n追加内容长度: {len(content)} 字符"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="更新飞书文档")
    parser.add_argument("--doc-id", required=True, help="文档 ID")
    parser.add_argument("--content", required=True, help="要追加的内容")
    args = parser.parse_args()
    try:
        print(update_document(args.doc_id, args.content))
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)
