"""飞书电子表格创建。"""
import argparse
import sys
from pathlib import Path

_FEISHU_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_FEISHU_ROOT))

from scripts.api import api_request


def create_sheet(title: str, folder_token: str = "") -> str:
    body = {"title": title}
    if folder_token:
        body["folder_token"] = folder_token

    data = api_request("POST", "/sheets/v3/spreadsheets", body=body, scopes=["sheets:spreadsheet"])
    sheet = data.get("data", {}).get("spreadsheet", {})
    token = sheet.get("spreadsheet_token", "")
    url = sheet.get("url", "")
    return f"表格创建成功\n标题: {title}\nToken: {token}\n链接: {url}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="创建飞书电子表格")
    parser.add_argument("--title", required=True, help="表格标题")
    parser.add_argument("--folder-token", default="", help="文件夹 token")
    args = parser.parse_args()
    try:
        print(create_sheet(args.title, args.folder_token))
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)
