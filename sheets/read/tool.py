"""飞书电子表格读取。"""
import argparse
import re
import sys
from pathlib import Path

_FEISHU_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_FEISHU_ROOT))

from scripts.api import api_request


def _parse_sheet_url(url: str) -> str:
    m = re.search(r"feishu\.cn/sheets/([A-Za-z0-9]+)", url)
    return m.group(1) if m else url


def read_sheet(token: str, range_str: str = "") -> str:
    # 如果没指定范围，先获取工作表列表
    if not range_str:
        meta = api_request("GET", f"/sheets/v3/spreadsheets/{token}/sheets/query")
        sheets = meta.get("data", {}).get("sheets", [])
        if not sheets:
            return "[error] 表格中没有工作表"
        sheet_id = sheets[0].get("sheet_id", "")
        title = sheets[0].get("title", "Sheet1")
        range_str = f"{sheet_id}"

    data = api_request("GET", f"/sheets/v2/spreadsheets/{token}/values/{range_str}")
    values = data.get("data", {}).get("valueRange", {}).get("values", [])

    if not values:
        return "表格数据为空。"

    lines = []
    for row in values:
        cells = [str(c) if c is not None else "" for c in row]
        lines.append("\t".join(cells))
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="读取飞书电子表格")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--token", help="电子表格 token")
    group.add_argument("--url", help="飞书表格 URL")
    parser.add_argument("--range", default="", help="读取范围 (如 Sheet1!A1:D10)")
    args = parser.parse_args()
    try:
        t = args.token or _parse_sheet_url(args.url)
        print(read_sheet(t, args.range))
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)
