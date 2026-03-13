"""飞书多维表格查询。"""
import argparse
import json
import re
import sys
from pathlib import Path

_FEISHU_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_FEISHU_ROOT))

from scripts.api import api_request


def _parse_bitable_url(url: str) -> str:
    m = re.search(r"feishu\.cn/base/([A-Za-z0-9]+)", url)
    return m.group(1) if m else url


def list_tables(app_token: str) -> str:
    data = api_request("GET", f"/bitable/v1/apps/{app_token}/tables")
    tables = data.get("data", {}).get("items", [])
    if not tables:
        return "没有数据表。"
    lines = [f"多维表格 {app_token} 共 {len(tables)} 个数据表:"]
    for i, t in enumerate(tables, 1):
        lines.append(f"{i}. {t.get('name', 'N/A')} (table_id: {t.get('table_id', '')})")
    return "\n".join(lines)


def query_records(app_token: str, table_id: str, filter_str: str = "", count: int = 20) -> str:
    params = {"page_size": count}
    if filter_str:
        params["filter"] = filter_str

    data = api_request("GET", f"/bitable/v1/apps/{app_token}/tables/{table_id}/records", params=params)
    records = data.get("data", {}).get("items", [])
    if not records:
        return "未找到记录。"

    lines = [f"共 {data.get('data', {}).get('total', len(records))} 条记录 (显示 {len(records)} 条):"]
    for i, rec in enumerate(records, 1):
        record_id = rec.get("record_id", "")
        fields = rec.get("fields", {})
        field_strs = []
        for k, v in fields.items():
            if isinstance(v, list):
                v = ", ".join(str(item.get("text", item) if isinstance(item, dict) else item) for item in v)
            field_strs.append(f"{k}: {v}")
        lines.append(f"{i}. [{record_id}] {' | '.join(field_strs)}")
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="查询飞书多维表格")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--app-token", help="多维表格 app_token")
    group.add_argument("--url", help="多维表格 URL")
    parser.add_argument("--table-id", help="数据表 ID")
    parser.add_argument("--list-tables", action="store_true", help="列出所有数据表")
    parser.add_argument("--filter", default="", help="筛选条件")
    parser.add_argument("--count", type=int, default=20, help="返回数量")
    args = parser.parse_args()
    try:
        token = args.app_token or _parse_bitable_url(args.url)
        if args.list_tables:
            print(list_tables(token))
        elif args.table_id:
            print(query_records(token, args.table_id, args.filter, args.count))
        else:
            print("[error] 需要 --table-id 或 --list-tables", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)
