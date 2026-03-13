"""飞书文件夹内容列表。"""
import argparse
import sys
from pathlib import Path

_FEISHU_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_FEISHU_ROOT))

from scripts.api import api_request

# 文件类型映射
_TYPE_MAP = {
    "file": "文件",
    "docx": "docx",
    "sheet": "sheet",
    "mindnote": "思维导图",
    "bitable": "多维表格",
    "folder": "文件夹",
    "slides": "幻灯片",
}


def list_folder(folder_token: str = "", count: int = 20) -> str:
    params = {"page_size": count}
    if folder_token:
        params["folder_token"] = folder_token

    # 使用 drive v1 API 列出文件
    path = f"/drive/v1/files"
    if folder_token:
        path = f"/drive/v1/files?folder_token={folder_token}&page_size={count}"
        data = api_request("GET", path)
    else:
        data = api_request("GET", "/drive/v1/files", params={"page_size": count})

    files = data.get("data", {}).get("files", [])
    if not files:
        return f"文件夹{'(根目录)' if not folder_token else folder_token} 为空。"

    lines = [f"文件夹: {folder_token or '根目录'} (共 {len(files)} 项)"]
    for i, f in enumerate(files, 1):
        ftype = _TYPE_MAP.get(f.get("type", ""), f.get("type", "unknown"))
        name = f.get("name", "N/A")
        token = f.get("token", "")
        lines.append(f"{i}. [{ftype}] {name} (token: {token})")

    has_more = data.get("data", {}).get("has_more", False)
    if has_more:
        lines.append(f"... 还有更多文件，增加 --count 参数获取更多")

    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="列出飞书文件夹内容")
    parser.add_argument("--folder-token", default="", help="文件夹 token，留空列出根目录")
    parser.add_argument("--count", type=int, default=20, help="返回数量")
    args = parser.parse_args()
    try:
        print(list_folder(args.folder_token, args.count))
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)
