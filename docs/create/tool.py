"""飞书文档创建。"""
import argparse
import sys
from pathlib import Path

_FEISHU_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_FEISHU_ROOT))

from scripts.api import api_request


def create_document(title: str, folder_token: str = "", content: str = "") -> str:
    body = {"title": title}
    if folder_token:
        body["folder_token"] = folder_token

    # 使用 user_access_token 创建，文档归属当前用户
    data = api_request("POST", "/docx/v1/documents", body=body, use_user_token=True)
    doc = data.get("data", {}).get("document", {})
    doc_id = doc.get("document_id", "")
    url = doc.get("url", "")

    # 如果提供了初始内容，追加到文档
    if content and doc_id:
        try:
            blocks_data = api_request("GET", f"/docx/v1/documents/{doc_id}/blocks",
                                      use_user_token=True)
            doc_block_id = blocks_data.get("data", {}).get("items", [{}])[0].get("block_id", doc_id)

            api_request("POST", f"/docx/v1/documents/{doc_id}/blocks/{doc_block_id}/children",
                        body={
                "children": [{
                    "block_type": 2,
                    "text": {
                        "elements": [{
                            "text_run": {"content": content, "text_element_style": {}}
                        }],
                        "style": {}
                    }
                }]
            }, use_user_token=True)
        except Exception:
            pass  # 内容追加失败不影响文档创建结果

    return f"文档创建成功\n标题: {title}\nID: {doc_id}\n链接: {url}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="创建飞书文档")
    parser.add_argument("--title", required=True, help="文档标题")
    parser.add_argument("--folder-token", default="", help="文件夹 token")
    parser.add_argument("--content", default="", help="初始正文内容")
    args = parser.parse_args()
    try:
        print(create_document(args.title, args.folder_token, args.content))
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)
