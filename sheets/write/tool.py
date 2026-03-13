"""飞书电子表格写入。"""
import argparse
import json
import sys
from pathlib import Path

_FEISHU_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_FEISHU_ROOT))

from scripts.api import api_request


def write_sheet(token: str, range_str: str, values: list) -> str:
    data = api_request("PUT", f"/sheets/v2/spreadsheets/{token}/values", body={
        "valueRange": {
            "range": range_str,
            "values": values,
        }
    })
    updated = data.get("data", {}).get("updatedCells", 0)
    return f"写入成功：范围 {range_str}，更新 {updated} 个单元格"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="写入飞书电子表格")
    parser.add_argument("--token", required=True, help="电子表格 token")
    parser.add_argument("--range", required=True, help="写入范围 (如 Sheet1!A1:B2)")
    parser.add_argument("--values", required=True, help="JSON 二维数组")
    args = parser.parse_args()
    try:
        values = json.loads(args.values)
        print(write_sheet(args.token, args.range, values))
    except json.JSONDecodeError as e:
        print(f"[error] values 不是合法 JSON: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)
